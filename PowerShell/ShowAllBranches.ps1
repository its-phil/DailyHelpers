if ($args.Count -eq 1)
{
    $rootDir = $args[0]
}
else
{
    $rootDir = "."    
}
Write-Host $("Root directory is $rootDir")

# Get the maximum directory name length for correct indentation
ForEach ($dir in Get-ChildItem -Directory -Path $rootDir)
{
    if (Test-Path "$($rootDir)\$($dir)\.git")
    {
        if ($dir.Name.Length -gt $maxWidth)
        {
            $maxWidth = $dir.Name.Length
        }
    }
}
$maxWidth = -$maxWidth - 2 # magic transformation ;)

# Print the current branch of all git repos
ForEach ($dir in Get-ChildItem -Directory -Path $rootDir) 
{
    if (Test-Path "$($rootDir)\$($dir)\.git")
    {
        Set-Location "$($rootDir)\$dir"
        
        $branch = Invoke-Expression "git rev-parse --abbrev-ref HEAD"
        Write-Host $( "> Directory {0,$($maxWidth)}" -f "$($dir):") -NoNewLine
        
        if ($branch -eq "master") 
        {
            Write-Host $branch -ForegroundColor Cyan
        }
        elseif ($branch -eq "develop")
        {
            Write-Host $branch -ForegroundColor Green
        }
        else
        {
            Write-Host $branch -ForegroundColor Yellow
        }

        Set-Location ..
    }
}

Read-Host -Prompt "Press Enter to exit"