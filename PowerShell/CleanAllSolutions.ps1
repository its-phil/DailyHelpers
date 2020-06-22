if ($args.Count -eq 1)
{
    $rootDir = $args[0]
}
else
{
    $rootDir = "."    
}
Write-Host $("Root directory is $rootDir")

# Print the current branch of all git repos
ForEach($dir in Get-ChildItem -Directory -Path $rootDir)
{
    ForEach($file in  Get-ChildItem -File -Filter "*.sln" -Path "$($rootDir)\$($dir)")
    {
        Write-Host $( "> Cleaning $($file):") -ForegroundColor Magenta
        dotnet clean "$($rootDir)\$($dir)\$($file)"
    }
}

Read-Host -Prompt "Press Enter to exit"