if ($args.Count -eq 1) {
    $rootDir = $args[0]
}
else {
    $rootDir = "."    
}
$rootDir = Resolve-Path $rootDir
Write-Host $("Root directory is $rootDir")

ForEach ($dir in Get-ChildItem -Directory -Path $rootDir) {
    $testPath = "$($dir)/.git"
    if (Test-Path $testPath) {
        Write-Host "> Pulling $($dir.Name)" -ForegroundColor Green
        Set-Location $dir
        git pull --all --prune
    }
    Set-Location $rootDir
}