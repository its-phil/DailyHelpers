if ($args.Count -eq 1) {
    $rootDir = $args[0]
}
else {
    $rootDir = "."    
}
$rootDir = Resolve-Path $rootDir
Write-Host $("Root directory is $rootDir")

# Get the maximum directory name length for correct indentation
ForEach ($dir in Get-ChildItem -Path $rootDir -Directory) {
    $testPath = "$($dir)/.git"
    if (Test-Path $testPath) {
        if ($dir.Name.Length -gt $maxWidth) {
            $maxWidth = $dir.Name.Length
        }
    }
}
$maxWidth = - $maxWidth - 2 # magic transformation ;)

# Print the current branch of all git repos
ForEach ($dir in Get-ChildItem -Path $rootDir -Directory) {
    $testPath = "$($dir)/.git"
    if (Test-Path -Path $testPath -PathType Container) {
        Set-Location $testPath
        
        $branch = Invoke-Expression "git rev-parse --abbrev-ref HEAD"
        Write-Host $( "> Directory ") -NoNewLine
        Write-Host $( "{0,$($maxWidth)}" -f "$($dir.Name)") -NoNewLine -ForegroundColor White
        
        if ($branch -eq "master") {
            Write-Host $branch -ForegroundColor Cyan
        }
        elseif ($branch -eq "develop") {
            Write-Host $branch -ForegroundColor Green
        }
        else {
            Write-Host $branch -ForegroundColor Yellow
        }
    }
    Set-Location $rootDir
}