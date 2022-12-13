
Add-Type -Assembly System.Windows.Forms

function CopyAndCreateShortCut($maxVersion)
{
    # maxスクリプトをコピー。
    #コピー元のフォルダのパス
    $copySrcFolder = "tkExporter_sub\*"
    #コピー先のフォルダのパス
    $copyDstFolder = $copyDstFolderPrefix
    

    if( Test-path $copyDstFolder){
        #コピー先のフォルダがあれば。
        #フォルダの内容をコピー。
        Copy-Item $copySrcFolder -Destination $copyDstFolder -Recurse -Force
    }
}

#アプリケーションデータのフォルダを取得。
$appData = [Environment]::GetFolderPath("ApplicationData")

#コピー先のフォルダを作成。
$copyDstFolderPrefix = $appData + "\Blender Foundation\Blender\3.3\scripts\addons\tkExporter_sub"
#フォルダを作成
New-Item $copyDstFolderPrefix -ItemType Directory



CopyAndCreateShortCut("3.3")
