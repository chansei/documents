$rtn = @{
    "TotalMemoryCapacity" = $null
    "TotalMemorySlot" = $null
    "ActiveMemorySlot" = $null
    "MemoryFrequency" = $null
}

# 物理メモリの合計
$rtn."TotalMemoryCapacity" = Get-WmiObject -Class Win32_PhysicalMemory | %{ $_.Capacity} | Measure-Object -Sum | %{($_.sum /1024/1024/1024).toString()+"GB"}
# 合計のメモリスロット数を取得する
$rtn."TotalMemorySlot" = Get-WmiObject -Class Win32_PhysicalMemoryArray | %{ $_.MemoryDevices} | Measure-Object -Sum | %{($_.sum).toString()}
# 使用中のメモリスロット数を取得する
$rtn."ActiveMemorySlot" = Get-WmiObject -Class Win32_PhysicalMemory | Measure-Object | %{ $_.Count} | Measure-Object -Sum | %{($_.sum).toString()}
# 物理メモリの周波数
$rtn."MemoryFrequency" = Get-WmiObject -Class Win32_PhysicalMemory | %{ $_.Speed} | Measure-Object -Average | %{($_.Average).toString()+"MHz"}

# 結果を表示
"TotalMemoryCapacity".PadRight(20)+"TotalMemorySlot".PadRight(20)+"ActiveMemorySlot".PadRight(20)+"MemoryFrequency".PadRight(20)
$rtn."TotalMemoryCapacity".PadRight(20)+$rtn."TotalMemorySlot".PadRight(20)+$rtn."ActiveMemorySlot".PadRight(20)+$rtn."MemoryFrequency".PadRight(20)+"`n"