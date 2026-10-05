@tool
extends EditorPlugin
## Ajusta o manifesto Android na exportação. A seção 14 permite só INTERNET,
## ACCESS_NETWORK_STATE e AD_ID; o SDK de anúncios acrescenta as permissões da
## API Privacy Sandbox (ACCESS_ADSERVICES_*), READ_BASIC_PHONE_STATE e uma
## cópia errada "android.permission.AD_ID", que este jogo não usa. Elas são
## removidas com tools:node="remove". tools/check_manifest.py confere o APK.

const REMOVED := [
	"android.permission.READ_BASIC_PHONE_STATE",
	"android.permission.AD_ID",
	"android.permission.ACCESS_ADSERVICES_AD_ID",
	"android.permission.ACCESS_ADSERVICES_ATTRIBUTION",
	"android.permission.ACCESS_ADSERVICES_TOPICS",
]

var _exporter: EditorExportPlugin


func _enter_tree() -> void:
	_exporter = ManifestExporter.new()
	add_export_plugin(_exporter)


func _exit_tree() -> void:
	remove_export_plugin(_exporter)


class ManifestExporter extends EditorExportPlugin:
	func _get_name() -> String:
		return "EsqueletonsManifest"

	func _supports_platform(platform: EditorExportPlatform) -> bool:
		return platform is EditorExportPlatformAndroid

	func _get_android_manifest_element_contents(_platform: EditorExportPlatform, _debug: bool) -> String:
		var out := PackedStringArray()
		for p in REMOVED:
			out.append('<uses-permission android:name="%s" tools:node="remove" />' % p)
		return "\n".join(out)
