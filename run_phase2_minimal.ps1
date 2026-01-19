# PowerShell version of Phase 2 Minimal
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "🚀 PHASE 2 MINIMAL - POWERSHELL VERSION" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan

# 1. Load data
Write-Host "`n1. 📂 LOADING DATA" -ForegroundColor Yellow
$dataPath = "data/processed/dev_subset_100.json"

if (-not (Test-Path $dataPath)) {
    Write-Host "❌ Data file not found: $dataPath" -ForegroundColor Red
    return
}

$data = Get-Content $dataPath | ConvertFrom-Json
Write-Host "✅ Loaded $($data.Count) examples" -ForegroundColor Green

# Show first example
if ($data -and $data[0]) {
    $first = $data[0]
    $keys = $first.PSObject.Properties.Name
    Write-Host "   First example has keys: $($keys[0..4] -join ', ')" -ForegroundColor Gray
    if ($first.question) {
        Write-Host "   Sample question: $($first.question.Substring(0, [Math]::Min(50, $first.question.Length)))..." -ForegroundColor Gray
    }
}

# 2. Create chunks
Write-Host "`n2. 🛠️ CREATING CHUNKS" -ForegroundColor Yellow
$chunks = @()

for ($i = 0; $i -lt [Math]::Min(20, $data.Count); $i++) {
    $example = $data[$i]
    
    $contextText = ""
    if ($example.context -and $example.context -is [Array]) {
        foreach ($item in $example.context) {
            if ($item -is [Array] -and $item.Count -ge 2) {
                $title = $item[0]
                $sentences = if ($item[1] -is [Array]) { $item[1] } else { @($item[1]) }
                $contextText += "$title`: $($sentences -join ' '). "
            }
        }
    }
    
    $chunk = @{
        chunk_id = "chunk_$i"
        text = if ($contextText.Length -gt 300) { $contextText.Substring(0, 300) } else { $contextText }
        question = if ($example.question -and $example.question.Length -gt 50) { 
            $example.question.Substring(0, 50) 
        } else { $example.question }
        answer = $example.answer
    }
    
    $chunks += $chunk
    
    if ($i -lt 2) {
        Write-Host "   Chunk $($i+1): $($contextText.Length) chars" -ForegroundColor Gray
    }
}

Write-Host "✅ Created $($chunks.Count) chunks" -ForegroundColor Green

# 3. "Build graph" (simulate)
Write-Host "`n3. 🕸️ BUILDING SIMPLE GRAPH" -ForegroundColor Yellow
Write-Host "   Simulating graph construction with $($chunks.Count) chunks" -ForegroundColor Gray

# Create directory for graph
$graphDir = "data/indices"
New-Item -ItemType Directory -Force -Path $graphDir | Out-Null
$graphPath = "$graphDir/simple_graph.txt"
"# Simple Graph File`n# Created at $(Get-Date)`n# Contains $($chunks.Count) chunks" | Out-File -FilePath $graphPath
Write-Host "💾 Graph info saved to $graphPath" -ForegroundColor Green

# 4. Test retrieval
Write-Host "`n4. 🔍 TESTING RETRIEVAL" -ForegroundColor Yellow
$testQueries = @("mathematician", "music", "art", "country")

foreach ($query in $testQueries) {
    $results = @()
    $queryLower = $query.ToLower()
    
    foreach ($chunk in $chunks[0..[Math]::Min(19, $chunks.Count-1)]) {
        if ($chunk.text -and $chunk.text.ToLower().Contains($queryLower)) {
            $results += $chunk
        }
    }
    
    Write-Host "   '$query': Found $($results.Count) results" -ForegroundColor Gray
    if ($results.Count -gt 0) {
        $text = $results[0].text
        $preview = if ($text.Length -gt 60) { $text.Substring(0, 60) + "..." } else { $text }
        Write-Host "     Top: $preview" -ForegroundColor Gray
    }
}

# 5. Simple evaluation
Write-Host "`n5. 📈 RUNNING SIMPLE EVALUATION" -ForegroundColor Yellow
$testPredictions = @()
$testGolds = @()

for ($i = 0; $i -lt [Math]::Min(10, $data.Count); $i++) {
    $example = $data[$i]
    $question = if ($example.question) { $example.question.ToLower() } else { "" }
    $answer = $example.answer
    
    # Simple rule-based prediction
    if ($question -match "mathematic") {
        $prediction = "mathematician"
    } elseif ($question -match "music|art") {
        $prediction = "art/music"
    } elseif ($question -match "country") {
        $prediction = "country"
    } else {
        $prediction = "unknown"
    }
    
    $testPredictions += $prediction
    $testGolds += $answer
}

# Calculate exact match
$exactMatches = 0
for ($i = 0; $i -lt $testPredictions.Count; $i++) {
    if ($testPredictions[$i] -eq $testGolds[$i]) {
        $exactMatches++
    }
}

$exactMatchScore = if ($testPredictions.Count -gt 0) { $exactMatches / $testPredictions.Count } else { 0 }
Write-Host "   Exact Match Score: $($exactMatchScore.ToString('0.000'))" -ForegroundColor Gray
Write-Host "   Tested on: $($testPredictions.Count) examples" -ForegroundColor Gray

# 6. Create summary
Write-Host "`n6. 📋 CREATING SUMMARY" -ForegroundColor Yellow
$summaryDir = "reports/phase2"
New-Item -ItemType Directory -Force -Path $summaryDir | Out-Null
$summaryPath = "$summaryDir/minimal_summary.txt"

$summary = @"
============================================================
PHASE 2 MINIMAL EXECUTION - SUCCESS (PowerShell Version)
============================================================
Data: $($data.Count) examples loaded
Chunks: $($chunks.Count) created
Graph: Simulated graph construction
Retrieval: Tested with keyword search
Evaluation: Basic metrics calculated
Exact Match Score: $($exactMatchScore.ToString('0.000'))

EXECUTION COMPLETED SUCCESSFULLY
============================================================
"@

$summary | Out-File -FilePath $summaryPath -Encoding UTF8
Write-Host "💾 Summary saved to $summaryPath" -ForegroundColor Green

# FINAL MESSAGE
Write-Host "`n" + ("="*60) -ForegroundColor Cyan
Write-Host "🎉 PHASE 2 MINIMAL COMPLETE!" -ForegroundColor Green
Write-Host "="*60 -ForegroundColor Cyan
Write-Host "✅ Data loaded and processed" -ForegroundColor Green
Write-Host "✅ Graph simulated and saved" -ForegroundColor Green
Write-Host "✅ Retrieval tested" -ForegroundColor Green
Write-Host "✅ Evaluation run" -ForegroundColor Green
Write-Host "✅ Summary created" -ForegroundColor Green
Write-Host "`n📧 READY TO EMAIL HAVVA!" -ForegroundColor Cyan
Write-Host "="*60 -ForegroundColor Cyan
