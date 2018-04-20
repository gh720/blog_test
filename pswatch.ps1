# this is intended to replace the sass file watcher which does not handle some workflows well

$title="file watcher window"
$proc = Get-Process | ? {$_.MainWindowTitle -eq $title }
if ($proc -ne $null) {
    $child = Get-WmiObject -Class Win32_Process -Filter "ParentProcessID=$($proc.id)"  | 
        ? { $_.ProcessName -eq 'powershell.exe' } |
        Select-Object -Property ProcessID, ProcessName
    if ($child -ne $null ) {
        echo "killing $($child.processid), $($child.processname)..."
        kill $child.processid -force
    }
}

$Host.UI.RawUI.WindowTitle = $title

$watcher = New-Object System.IO.FileSystemWatcher
$watcher.Path = ".\static\scss"
$watcher.Filter = "*.scss"
$watcher.IncludeSubdirectories = $true
$watcher.EnableRaisingEvents = $true  

$global:last_read = [DateTime]::MinValue
$global:input_part="\\static\\scss"
$global:output_part = "\static\css" 
$global:input_ext="\.scss$"
$global:output_ext=".css"

$action = { 
    try {
    $path = $Event.SourceEventArgs.FullPath
    $last_w= [datetime](Get-ItemProperty -Path $path -Name LastWriteTime).lastwritetime
    $last_c = [datetime](Get-ItemProperty -Path $path -Name CreationTime).creationtime
    if ($last_c -gt $last_w) { $last_w= $last_c }
    $changeType = $Event.SourceEventArgs.ChangeType
    $logline = "$(Get-Date), $changeType, $path, $($global:last_read), $last_w"
    Add-content ".\log.txt" -value $logline
    if ($global:last_read -lt $last_w) {
        $m_path=$path -replace $global:input_part, $global:output_part 
        $output_path=$m_path -replace $global:input_ext, $global:output_ext
      $changeType = $Event.SourceEventArgs.ChangeType
      $logline = "processing $($changeType): cmd /c sass --scss $path | perl .\fix.pl > $output_path 2>&1"
      Add-content ".\log.txt" -value $logline
            #$arg = "`"$path`":`"$output_path`""
        cmd "/c sass --scss $path 2>&1 | perl .\fix.pl > $output_path"
    }
    $global:last_read=$last_w
    }
    catch [Exception] {
        Add-content ".\log.txt" -value "$($_.Exception.GetType().FullName), $($_.Exception.Message)"
    }
}
Register-ObjectEvent $watcher "Created" -Action $action
Register-ObjectEvent $watcher "Changed" -Action $action
#    Register-ObjectEvent $watcher "Deleted" -Action $action
Register-ObjectEvent $watcher "Renamed" -Action $action
while ($true) {sleep 1}
