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
Get-ChildItem -Directory -Path $rootDir | Foreach-Object {
    if (Test-Path "$($rootDir)\$($_)\.git")
    {
        if ($_.Name.Length -gt $maxWidth)
        {
            $maxWidth = $_.Name.Length
        }
    }
}
$maxWidth = -$maxWidth - 2 # magic transformation ;)

# Print the current branch of all git repos
Get-ChildItem -Directory -Path $rootDir | Foreach-Object {
    if (Test-Path "$($rootDir)\$($_)\.git")
    {
        Set-Location "$($rootDir)\$_"
        
        $branch = Invoke-Expression "git rev-parse --abbrev-ref HEAD"
        Write-Host $( "> Directory {0,$($maxWidth)}" -f "$($_):") -NoNewLine
        
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