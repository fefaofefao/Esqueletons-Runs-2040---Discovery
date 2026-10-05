extends Node
## Ponte com o plugin AdMob (Poing Studios, addons/admob). Só é carregada no
## Android, pelo autoload Ads. Fluxo: UMP (consentimento) -> RequestConfiguration
## (público 13+, não infantil) -> MobileAds.initialize -> pré-carrega anúncios.

signal interstitial_closed
signal rewarded_closed(granted: bool)
signal privacy_closed

var _ids: Dictionary = {}
var _audience: Dictionary = {}
var _initialized := false
var _banner: AdView = null
var _banner_wanted := false
var _interstitial: InterstitialAd = null
var _rewarded: RewardedAd = null
var _earned := false


func start(ids: Dictionary, audience: Dictionary) -> void:
	_ids = ids
	_audience = audience
	var params := ConsentRequestParameters.new()
	params.tag_for_under_age_of_consent = bool(audience.get("under_age_of_consent", false))
	UserMessagingPlatform.consent_information.update(params, _on_consent_info, func(_e: FormError) -> void: _init_sdk())


func _on_consent_info() -> void:
	var ci := UserMessagingPlatform.consent_information
	if ci.get_is_consent_form_available() and ci.get_consent_status() == ConsentInformation.ConsentStatus.REQUIRED:
		UserMessagingPlatform.load_consent_form(
			func(form: ConsentForm) -> void: form.show(func(_e: FormError) -> void: _init_sdk()),
			func(_e: FormError) -> void: _init_sdk())
	else:
		_init_sdk()


func _can_request() -> bool:
	var st := UserMessagingPlatform.consent_information.get_consent_status()
	return st == ConsentInformation.ConsentStatus.OBTAINED or st == ConsentInformation.ConsentStatus.NOT_REQUIRED


func _init_sdk() -> void:
	if _initialized or not _can_request():
		return
	var rc := RequestConfiguration.new()
	rc.tag_for_child_directed_treatment = (RequestConfiguration.TagForChildDirectedTreatment.TRUE
		if bool(_audience.get("child_directed", false)) else RequestConfiguration.TagForChildDirectedTreatment.FALSE)
	rc.tag_for_under_age_of_consent = (RequestConfiguration.TagForUnderAgeOfConsent.TRUE
		if bool(_audience.get("under_age_of_consent", false)) else RequestConfiguration.TagForUnderAgeOfConsent.FALSE)
	rc.max_ad_content_rating = str(_audience.get("max_rating", "T"))
	MobileAds.set_request_configuration(rc)
	var listener := OnInitializationCompleteListener.new()
	listener.on_initialization_complete = func(_s: InitializationStatus) -> void:
		_initialized = true
		_load_interstitial()
		_load_rewarded()
		set_banner_visible(_banner_wanted)
	MobileAds.initialize(listener)


func ready_for_ads() -> bool:
	return _initialized


# ------------------------------------------------------------------ banner
func set_banner_visible(v: bool) -> void:
	_banner_wanted = v
	if not _initialized:
		return
	if v:
		if _banner == null:
			_banner = AdView.new(str(_ids.get("banner", "")), AdSize.new(320, 50), AdPosition.TOP)
			_banner.load_ad(AdRequest.new())
		_banner.show()
	elif _banner:
		_banner.hide()


# ------------------------------------------------------------------ intersticial (sempre pré-carregado)
func _load_interstitial() -> void:
	var cb := InterstitialAdLoadCallback.new()
	cb.on_ad_loaded = func(ad: InterstitialAd) -> void:
		_interstitial = ad
		ad.full_screen_content_callback.on_ad_dismissed_full_screen_content = func() -> void:
			_interstitial = null
			interstitial_closed.emit()
			_load_interstitial()
		ad.full_screen_content_callback.on_ad_failed_to_show_full_screen_content = func(_e: AdError) -> void:
			_interstitial = null
			interstitial_closed.emit()
			_load_interstitial()
	cb.on_ad_failed_to_load = func(_e: LoadAdError) -> void:
		get_tree().create_timer(60.0).timeout.connect(_load_interstitial)
	InterstitialAdLoader.new().load(str(_ids.get("interstitial", "")), AdRequest.new(), cb)


func interstitial_ready() -> bool:
	return _interstitial != null


func show_interstitial() -> void:
	if _interstitial:
		_interstitial.show()
	else:
		interstitial_closed.emit.call_deferred()


# ------------------------------------------------------------------ premiado
func _load_rewarded() -> void:
	var cb := RewardedAdLoadCallback.new()
	cb.on_ad_loaded = func(ad: RewardedAd) -> void:
		_rewarded = ad
		ad.full_screen_content_callback.on_ad_dismissed_full_screen_content = func() -> void:
			_rewarded = null
			# a recompensa chega por callback próprio; espera um quadro para lê-la
			(func() -> void: rewarded_closed.emit(_earned)).call_deferred()
			_load_rewarded()
		ad.full_screen_content_callback.on_ad_failed_to_show_full_screen_content = func(_e: AdError) -> void:
			_rewarded = null
			rewarded_closed.emit(false)
			_load_rewarded()
	cb.on_ad_failed_to_load = func(_e: LoadAdError) -> void:
		get_tree().create_timer(60.0).timeout.connect(_load_rewarded)
	RewardedAdLoader.new().load(str(_ids.get("rewarded", "")), AdRequest.new(), cb)


func rewarded_ready() -> bool:
	return _rewarded != null


func show_rewarded() -> void:
	if _rewarded == null:
		rewarded_closed.emit.call_deferred(false)
		return
	_earned = false
	var listener := OnUserEarnedRewardListener.new()
	listener.on_user_earned_reward = func(_item: RewardedItem) -> void: _earned = true
	_rewarded.show(listener)


# ------------------------------------------------------------------ privacidade
func privacy_required() -> bool:
	return (UserMessagingPlatform.consent_information.get_privacy_options_requirement_status()
		== ConsentInformation.PrivacyOptionsRequirementStatus.REQUIRED)


func show_privacy() -> void:
	UserMessagingPlatform.show_privacy_options_form(func(_e: FormError) -> void:
		_init_sdk()
		privacy_closed.emit())
