param(
    [Parameter(Mandatory=$true)]
    [ValidateSet('Install','Uninstall')]
    [string]$Action
)

$ErrorActionPreference='Stop'
$packageDir=$PSScriptRoot
$infName='Nikon8000-9000-x64.inf'
$infPath=Join-Path $packageDir ('Driver\'+$infName)
$catPath=Join-Path $packageDir 'Driver\Nikon8000-9000-x64.cat'
$certificatePath=Join-Path $packageDir 'Nikon8000-9000-LocalSigner.cer'
$expectedThumbprint='17124401603110A5F91704BB536493C0BE336944'
$logDir=Join-Path $packageDir 'Logs'
$logPath=Join-Path $logDir ($Action+'.log')
$transcriptStarted=$false
$exitCode=0

try {
    if ($env:PROCESSOR_ARCHITECTURE -ne 'AMD64') {
        throw '本包需要在 Intel/AMD x64 版 Windows 11 中运行。'
    }
    $osInfo=Get-ItemProperty -LiteralPath 'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion'
    if ($osInfo.CurrentMajorVersionNumber -ne 10 -or [int]$osInfo.CurrentBuildNumber -lt 22000) {
        throw '本包用于 Windows 11，请核对当前系统版本。'
    }

    $identity=[Security.Principal.WindowsIdentity]::GetCurrent()
    $principal=[Security.Principal.WindowsPrincipal]::new($identity)
    if (-not $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
        Write-Host '正在请求管理员权限，请在 Windows 提示中点击“是”。'
        $arguments='-NoProfile -ExecutionPolicy Bypass -File "{0}" -Action {1}' -f $PSCommandPath,$Action
        $process=Start-Process -FilePath "$env:WINDIR\System32\WindowsPowerShell\v1.0\powershell.exe" -ArgumentList $arguments -Verb RunAs -WindowStyle Hidden -Wait -PassThru
        if (Test-Path -LiteralPath $logPath) {
            Get-Content -LiteralPath $logPath -Encoding UTF8 | ForEach-Object { Write-Host $_ }
        }
        exit $process.ExitCode
    }

    New-Item -ItemType Directory -Path $logDir -Force | Out-Null
    Start-Transcript -LiteralPath $logPath -Force | Out-Null
    $transcriptStarted=$true
    Write-Host 'Nikon SUPER COOLSCAN 8000 ED / 9000 ED — Windows 11 x64'

    if ($Action -eq 'Install') {
        Write-Host '正在核对安装文件和本地签名。'
        $certificate=[Security.Cryptography.X509Certificates.X509Certificate2]::new($certificatePath)
        if ($certificate.Thumbprint -ne $expectedThumbprint) {
            throw '公共证书与本包不匹配，请重新解压完整安装包。'
        }
        $catalogStatus=Test-FileCatalog -Path $infPath -CatalogFilePath $catPath
        if ($catalogStatus -ne 'Valid') {
            throw 'INF 与签名目录的哈希不匹配，请重新解压完整安装包。'
        }
        Import-Certificate -FilePath $certificatePath -CertStoreLocation 'Cert:\LocalMachine\Root' | Out-Null
        Import-Certificate -FilePath $certificatePath -CertStoreLocation 'Cert:\LocalMachine\TrustedPublisher' | Out-Null
        $signature=Get-AuthenticodeSignature -LiteralPath $catPath
        if ($signature.Status -ne 'Valid' -or $signature.SignerCertificate.Thumbprint -ne $expectedThumbprint) {
            throw ('签名验证未通过：'+$signature.StatusMessage)
        }

        Write-Host '正在将驱动包加入 Windows，并匹配已连接的扫描仪。'
        & "$env:WINDIR\System32\pnputil.exe" /add-driver $infPath /install
        $nativeExitCode=$LASTEXITCODE
        if ($nativeExitCode -notin @(0,3010)) {
            throw ('Windows 安装命令失败，退出码：'+$nativeExitCode)
        }
        $exitCode=$nativeExitCode
        $registeredPackages=@(Get-WindowsDriver -Online | Where-Object {
            [IO.Path]::GetFileName($_.OriginalFileName) -ieq $infName
        })
        if ($registeredPackages.Count -eq 0) {
            throw '未在 Windows 驱动库中找到本包，请查看安装日志。'
        }
        $publishedNames=@($registeredPackages | ForEach-Object { $_.Driver })
        Write-Host ('驱动库中的包名称：'+($publishedNames -join ', '))

        $scanners=@(Get-PnpDevice -PresentOnly | Where-Object {
            $_.InstanceId -match '^SBP2\\NIKON___&LS-(8000|9000)_ED_'
        })
        $deviceResults=@(foreach ($scanner in $scanners) {
            $problem=Get-PnpDeviceProperty -InstanceId $scanner.InstanceId -KeyName DEVPKEY_Device_ProblemCode
            $driver=Get-PnpDeviceProperty -InstanceId $scanner.InstanceId -KeyName DEVPKEY_Device_DriverInfPath
            [pscustomobject]@{
                Device=$scanner.FriendlyName
                Status=$scanner.Status.ToString()
                ProblemCode=[int]$problem.Data
                DriverInf=$driver.Data
                UsingThisPackage=($driver.Data -in $publishedNames)
            }
        })
        [pscustomobject]@{
            Action=$Action
            DriverStoreAdded=$true
            PublishedNames=$publishedNames
            CertificateThumbprint=$expectedThumbprint
            RebootRequired=($nativeExitCode -eq 3010)
            Devices=$deviceResults
        } | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath (Join-Path $logDir 'Install-result.json') -Encoding UTF8

        if ($deviceResults.Count -eq 0) {
            Write-Host '驱动包已加入驱动库。目前未发现已连接的 8000 ED / 9000 ED。'
            Write-Host '连接 IEEE 1394 数据线并打开扫描仪电源后，Windows 将尝试自动匹配。'
        } else {
            $deviceResults | Format-Table Device,Status,ProblemCode,DriverInf,UsingThisPackage -AutoSize | Out-Host
            if (@($deviceResults | Where-Object { $_.ProblemCode -ne 0 }).Count -gt 0) {
                throw '驱动包已加入，但设备仍有错误代码。请根据上表和日志继续排查。'
            }
            if (@($deviceResults | Where-Object { -not $_.UsingThisPackage }).Count -gt 0) {
                Write-Warning '部分设备仍使用其他驱动包；当前实际使用的 INF 已列在上表。'
            }
            Write-Host '设备状态核对完成。问题代码 0 表示设备已正常启动。'
        }
        Write-Host '可以打开 Nikon Scan 核对扫描仪识别和预览。实际扫描需另行验证。'
    } else {
        Write-Host '正在查找本安装包。'
        $registeredPackages=@(Get-WindowsDriver -Online | Where-Object {
            [IO.Path]::GetFileName($_.OriginalFileName) -ieq $infName
        })
        foreach ($driverPackage in $registeredPackages) {
            Write-Host ('正在卸载：'+$driverPackage.Driver)
            & "$env:WINDIR\System32\pnputil.exe" /delete-driver $driverPackage.Driver /uninstall
            $nativeExitCode=$LASTEXITCODE
            if ($nativeExitCode -notin @(0,3010)) {
                throw ('Windows 卸载命令失败，退出码：'+$nativeExitCode+'。本包证书保留。')
            }
            if ($nativeExitCode -eq 3010) { $exitCode=3010 }
        }
        $remainingPackages=@(Get-WindowsDriver -Online | Where-Object {
            [IO.Path]::GetFileName($_.OriginalFileName) -ieq $infName
        })
        if ($remainingPackages.Count -gt 0) {
            throw '驱动库中仍存在本包。本包证书保留，请查看日志。'
        }
        foreach ($store in @('TrustedPublisher','Root')) {
            $certificateStorePath='Cert:\LocalMachine\'+$store+'\'+$expectedThumbprint
            if (Test-Path -LiteralPath $certificateStorePath) {
                Remove-Item -LiteralPath $certificateStorePath
            }
        }
        Write-Host '本驱动包及其公共信任证书已移除。电脑上原有的其他驱动包保留。'
    }

    if ($exitCode -eq 3010) {
        Write-Host 'Windows 要求重启才能完成操作。请保存工作后手动重启。'
    }
    Write-Host ('日志位置：'+$logPath)
} catch {
    Write-Host ('操作未完成：'+$_.Exception.Message) -ForegroundColor Red
    if ($_.Exception.NativeErrorCode -eq 1223) {
        Write-Host '管理员授权被取消。再次运行时请允许 Windows 提升权限。'
    }
    $exitCode=1
} finally {
    if ($transcriptStarted) { Stop-Transcript | Out-Null }
}
exit $exitCode

# SIG # Begin signature block
# MIIF2gYJKoZIhvcNAQcCoIIFyzCCBccCAQExDzANBglghkgBZQMEAgEFADB5Bgor
# BgEEAYI3AgEEoGswaTA0BgorBgEEAYI3AgEeMCYCAwEAAAQQH8w7YFlLCE63JNLG
# KX7zUQIBAAIBAAIBAAIBAAIBADAxMA0GCWCGSAFlAwQCAQUABCBKM4j2+SY4ZVWr
# +WMKLZPUaZtvp+cvTZXcqzD2GAwt26CCAzgwggM0MIICHKADAgECAhBJWtsiQDDq
# nkF1qJMD3Ru0MA0GCSqGSIb3DQEBCwUAMDIxMDAuBgNVBAMMJ0xvY2FsIE5pa29u
# IDgwMDAgRUQgOTAwMCBFRCBJTkYgUGFja2FnZTAeFw0yNjEwMDQxNDEzMjFaFw0z
# MTEwMDQxNDIzMjFaMDIxMDAuBgNVBAMMJ0xvY2FsIE5pa29uIDgwMDAgRUQgOTAw
# MCBFRCBJTkYgUGFja2FnZTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEB
# ANloD12gyN6rG4tLfr+UVq2PDq15k87mpfsPm8SRX/FC25REwaXIWkZCUnemuiWW
# dYeqJHHnb9r9wzo4rHEcwlUNKfoNnsL29tIOgkqA17Ew9L+TAPtITiw3ZY75H/wG
# nvzZtIFqz4f+KJZbFjjYf5F/0GedsnbP95uHfkHv+CfRe5Mdf0bDdURRfnFtJ4B/
# LNKI9tPijSxb5D60cuQ/ywVyrMaxCANXnBCoiAPh7450ElX9gHIqmvRT9jhnrVo7
# bGfOg8dQe1BwrFrR+3RZ2HWc6wIErJYWO/QYcJDxK0lCmiGQqj4XPV0tfLzUxjmh
# t1B88z3tLEsb0YL1ok4Xk/ECAwEAAaNGMEQwDgYDVR0PAQH/BAQDAgeAMBMGA1Ud
# JQQMMAoGCCsGAQUFBwMDMB0GA1UdDgQWBBQyvbU/Waz2v0b2F7VjiedAxtjLxzAN
# BgkqhkiG9w0BAQsFAAOCAQEAPZxUNq8USZcNqQqz3n3xANshrFou8tE4Q7cSgsiK
# LSRy5/zCImsNXa/vZwS+Rm89eRbo+2rvEPoFEqXOF9KrmCzJwgkcD6D7deYFk9Px
# m7k1bcX1aEQvecq99mmIfqrV/ko4C7XUNyI4RzCr5cVTeWAIPUZplO3PcjWymLpJ
# N3t0do5kiL8yj5npbeNjKgiF0eLifRvfpixlGu9R0neKf8Cy8vr01hbzg0mxsCRi
# qtNhpsGsbRyhsqSpxA2pTYyTBiVipIriQBtjBJ0rVE13hyFXWBmQ4YbpGVHjCI5p
# SM589dYg3iq/j0h3xuZtAlPl6BfAC3GiFJ5JZkJYUSNaujGCAfgwggH0AgEBMEYw
# MjEwMC4GA1UEAwwnTG9jYWwgTmlrb24gODAwMCBFRCA5MDAwIEVEIElORiBQYWNr
# YWdlAhBJWtsiQDDqnkF1qJMD3Ru0MA0GCWCGSAFlAwQCAQUAoIGEMBgGCisGAQQB
# gjcCAQwxCjAIoAKAAKECgAAwGQYJKoZIhvcNAQkDMQwGCisGAQQBgjcCAQQwHAYK
# KwYBBAGCNwIBCzEOMAwGCisGAQQBgjcCARUwLwYJKoZIhvcNAQkEMSIEIK9r54yc
# vrYzGp+fifiezTMz/xcNVTUEFtMMdP3aLjtlMA0GCSqGSIb3DQEBAQUABIIBABdS
# He1KNb9OFhaaJKrZ1CtixIzu9Ije2pvv2Q38FENfwBTYQrUZsnNTfOBxBnZ+Dka+
# C+U+ola9Sjq36vgsBHtWvGAfK1H005wZYa4PMhsY7vxgotq1Ckvd3wV7DRP8rtgl
# /PfEuLdwdHRfUNnZZshJh5nXGD6UCYw/rIGEVsAxQtsmy7hPmDrX51z6elq89ZLv
# krDmwzlTlSqp0i2P8Yg9Udt51iPivoHU4t5+wxzsav5YulJMVLfqliogmkPPc0wp
# jcQg1CQ8DhXjP0iXvYtwLU/WuMr33LRigETwvbUBmh/9E968kiLGXsAvu587lMqx
# Um29F+bxMCjdBtzDQG4=
# SIG # End signature block
