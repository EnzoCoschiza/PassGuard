param(
    [ValidateSet("all", "backend", "frontend")]
    [string]$Scope = "all",

    [switch]$InstallDeps
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$frontendRoot = Join-Path $repoRoot "frontend"
$localCacheRoot = Join-Path $repoRoot ".cache"
$uvCacheRoot = Join-Path $localCacheRoot "uv"

$results = New-Object System.Collections.Generic.List[object]

New-Item -ItemType Directory -Force -Path $uvCacheRoot | Out-Null
$env:UV_CACHE_DIR = $uvCacheRoot

function Invoke-Step {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Name,

        [Parameter(Mandatory = $true)]
        [string]$Command,

        [Parameter(Mandatory = $true)]
        [string]$WorkingDirectory
    )

    Write-Host ""
    Write-Host "==> $Name" -ForegroundColor Cyan
    Write-Host "    $Command" -ForegroundColor DarkGray

    Push-Location $WorkingDirectory
    try {
        Invoke-Expression $Command
        $exitCode = $LASTEXITCODE
    } finally {
        Pop-Location
    }

    if ($exitCode -eq 0) {
        Write-Host "PASS: $Command" -ForegroundColor Green
        $results.Add([pscustomobject]@{
                Name = $Name
                Command = $Command
                Status = "PASS"
            })
        return
    }

    Write-Host "FAIL: $Command" -ForegroundColor Red
    $results.Add([pscustomobject]@{
            Name = $Name
            Command = $Command
            Status = "FAIL"
        })
    throw "Step failed: $Name"
}

try {
    Write-Host "PassGuard CI local runner" -ForegroundColor Yellow
    Write-Host "Scope: $Scope" -ForegroundColor Yellow
    Write-Host "UV cache: $env:UV_CACHE_DIR" -ForegroundColor Yellow

    if ($Scope -in @("all", "backend")) {
        if ($InstallDeps) {
            Invoke-Step -Name "Install backend dependencies" -Command "uv sync --dev" -WorkingDirectory $repoRoot
        }

        Invoke-Step -Name "Backend lint" -Command "uv run ruff check ." -WorkingDirectory $repoRoot
        Invoke-Step -Name "Backend tests" -Command "uv run pytest" -WorkingDirectory $repoRoot
    }

    if ($Scope -in @("all", "frontend")) {
        if ($InstallDeps) {
            Invoke-Step -Name "Install frontend dependencies" -Command "npm ci" -WorkingDirectory $frontendRoot
        }

        Invoke-Step -Name "Frontend lint" -Command "npm run lint" -WorkingDirectory $frontendRoot
        Invoke-Step -Name "Frontend tests" -Command "npm run test" -WorkingDirectory $frontendRoot
        Invoke-Step -Name "Frontend build" -Command "npm run build" -WorkingDirectory $frontendRoot
    }

    Write-Host ""
    Write-Host "Summary" -ForegroundColor Yellow
    $results | Format-Table -AutoSize
} catch {
    Write-Host ""
    Write-Host "Summary" -ForegroundColor Yellow
    if ($results.Count -gt 0) {
        $results | Format-Table -AutoSize
    }

    Write-Error $_
    exit 1
}
