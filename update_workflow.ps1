$dir = 'c:\Users\mohda\OneDrive\Desktop\n8n workflow\Justcookdaily.com'
$files = Get-ChildItem -Path $dir -Filter '*.json'
Write-Host "Found $($files.Count) JSON files"
$f = $files[0]
Write-Host "Processing: $($f.Name) ($($f.Length) bytes)"

$bytes = [System.IO.File]::ReadAllBytes($f.FullName)
$content = [System.Text.Encoding]::UTF8.GetString($bytes)
Write-Host "Content length: $($content.Length) chars"

if ($content.Length -lt 10000) {
    Write-Host "ERROR: File too small"
    exit 1
}

# Verify it still has old values
Write-Host "Has old Gemini key: $($content.Contains('AIzaSyB4uaZKUCdVsr-RTHCSqfRr4_Pc0C9oJDk'))"
Write-Host "Has justcookdaily: $($content.Contains('justcookdaily.com'))"

# Apply all replacements
$content = $content.Replace('AIzaSyB4uaZKUCdVsr-RTHCSqfRr4_Pc0C9oJDk', 'AIzaSyCnYPk6n5X3KM41fywRqsDCDbKki5ZNLuQ')
$content = $content.Replace('lsxGULh0YmwITJ7q7lEdpROYPbyalyCglIOmJLkKgeIf5QeH5qTvtzUs', '3283013-61ec8888bf69be36008d30ad4')
$content = $content.Replace('https://justcookdaily.com', 'https://texasdadcooks.com')
$content = $content.Replace('"value": "bf149a"', '"value": "Texas Dad"')
$content = $content.Replace('nQq4 nD4T rPtF xb3C eMw6 iw2s', 'wew2 iL0F LJiH BPxB 0xzs Bqum')
$content = $content.Replace('justcookdaily.com', 'texasdadcooks.com')
$content = $content.Replace('JustCookDaily', 'TexasDadCooks')
$content = $content.Replace('pexels_api_key', 'pixabay_api_key')
$content = $content.Replace('_pexelsKey', '_pixabayKey')
$content = $content.Replace('  27: [ // Quick', '  1: [ // Quick')
$content = $content.Replace('  28: [ // Breakfast', '  39: [ // Breakfast')
$content = $content.Replace('  29: [ // Lunch', '  40: [ // Lunch')
$content = $content.Replace('  30: [ // Dinner', '  41: [ // Dinner')
$content = $content.Replace('  31: [ // Healthy', '  42: [ // Healthy')
$content = $content.Replace('  32: [ // Vegetarian', '  43: [ // Vegetarian')
$content = $content.Replace('  33: [ // Desserts', '  44: [ // Desserts')
$content = $content.Replace('  34: [ // Snacks', '  45: [ // Snacks')
$content = $content.Replace('  35: [ // Beverages', '  46: [ // Beverages')
$content = $content.Replace('id: 27, name:', 'id: 1, name:')
$content = $content.Replace('id: 28, name:', 'id: 39, name:')
$content = $content.Replace('id: 29, name:', 'id: 40, name:')
$content = $content.Replace('id: 30, name:', 'id: 41, name:')
$content = $content.Replace('id: 31, name:', 'id: 42, name:')
$content = $content.Replace('id: 32, name:', 'id: 43, name:')
$content = $content.Replace('id: 33, name:', 'id: 44, name:')
$content = $content.Replace('id: 34, name:', 'id: 45, name:')
$content = $content.Replace('id: 35, name:', 'id: 46, name:')
$content = $content.Replace('[27,28,29,30,31,32,33,34,35,36]', '[1,39,40,41,42,43,44,45,46,36]')
$content = $content.Replace('[1,39,40,41,42,43,44,45,46,36]', '[1,36,39,40,41,42,43,44,45,46]')
$content = $content.Replace('CATEGORY_FEEDS[27]', 'CATEGORY_FEEDS[1]')
$content = $content.Replace('CATEGORY_FALLBACK_POOL[27]', 'CATEGORY_FALLBACK_POOL[1]')
$content = $content.Replace('category_id: 27', 'category_id: 1')
$content = $content.Replace('bf149a @', 'Texas Dad @')

# Write back
[System.IO.File]::WriteAllBytes($f.FullName, [System.Text.Encoding]::UTF8.GetBytes($content))
Write-Host "SAVED successfully - $($content.Length) chars"

# Verify
Write-Host "--- VERIFICATION ---"
Write-Host "Has texasdadcooks: $($content.Contains('texasdadcooks.com'))"
Write-Host "Has new Gemini key: $($content.Contains('AIzaSyCnYPk6n5X3KM41fywRqsDCDbKki5ZNLuQ'))"  
Write-Host "Has pixabay key: $($content.Contains('3283013-61ec8888bf69be36008d30ad4'))"
Write-Host "Has Texas Dad: $($content.Contains('Texas Dad'))"
Write-Host "Has new WP pass: $($content.Contains('wew2 iL0F LJiH BPxB 0xzs Bqum'))"
Write-Host "OLD justcookdaily gone: $(-not $content.Contains('justcookdaily'))"
Write-Host "Cat ID 1: $($content.Contains('id: 1, name:'))"
Write-Host "Cat ID 39: $($content.Contains('id: 39, name:'))"
