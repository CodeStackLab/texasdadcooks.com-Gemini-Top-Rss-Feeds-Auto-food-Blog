$dir = 'c:\Users\mohda\OneDrive\Desktop\n8n workflow\Justcookdaily.com'
$f = (Get-ChildItem -Path $dir -Filter '*.json')[0]
$bytes = [System.IO.File]::ReadAllBytes($f.FullName)
$c = [System.Text.Encoding]::UTF8.GetString($bytes)

try { $null = $c | ConvertFrom-Json; Write-Host "VALID JSON" } catch { Write-Host "INVALID JSON: $_" }

Write-Host "texasdadcooks.com: $($c.Contains('texasdadcooks.com'))"
Write-Host "Texas Dad: $($c.Contains('Texas Dad'))"
Write-Host "New Gemini key: $($c.Contains('AIzaSyCnYPk6n5X3KM41fywRqsDCDbKki5ZNLuQ'))"
Write-Host "Pixabay key: $($c.Contains('55454132-b1ac9c8f692bf278b4b666ba2'))"
Write-Host "New WP pass: $($c.Contains('wew2 iL0F LJiH BPxB 0xzs Bqum'))"
Write-Host "OLD justcookdaily still present: $($c.Contains('justcookdaily'))"
Write-Host "OLD bf149a still present: $($c.Contains('bf149a'))"
Write-Host "Cat ID 1 present: $($c.Contains('id: 1, name:'))"
Write-Host "Cat ID 39 present: $($c.Contains('id: 39,'))"
Write-Host "Cat ID 41 present: $($c.Contains('id: 41,'))"
Write-Host "pixabay_api_key: $($c.Contains('pixabay_api_key'))"
