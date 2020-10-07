if ($args.Count -eq 1)
{
    $rootDir = $args[0]
}
else
{
    $rootDir = "."    
}
Write-Host $("Root directory is $rootDir")

ForEach ($dir in Get-ChildItem -Directory -Path $rootDir)
{
    if (Test-Path "$($rootDir)\$($dir)\.git")
    {
        Write-Host "> Pulling $($dir)" -ForegroundColor Green
        Set-Location "$($rootDir)\$dir"
        git pull --all --prune
        Set-Location ..
    }
}

Read-Host -Prompt "Press Enter to exit"