@echo off
echo [1/5] 產生 manifest...
python generate_manifest.py
if errorlevel 1 (
  echo 錯誤：generate_manifest.py 執行失敗
  echo 按任何鍵離開...
  pause >nul
  exit /b 1
)

echo [2/5] git add...
git add -A

echo [3/5] git commit...
for /f "tokens=1-2 delims= " %%a in ('wmic os get LocalDateTime /value ^| find "="') do set DT=%%b
set STAMP=%DT:~0,4%-%DT:~4,2%-%DT:~6,2% %DT:~8,2%:%DT:~10,2%:%DT:~12,2%
git commit -m "update %STAMP%"
if errorlevel 1 (
  echo 沒有需要 commit 的變更，跳過。
)

echo [4/5] git pull（同步遠端）...
git pull --rebase
if errorlevel 1 (
  echo 錯誤：git pull 失敗，可能有衝突需手動處理
  echo 按任何鍵離開...
  pause >nul
  exit /b 1
)

echo [5/5] git push...
git push
if errorlevel 1 (
  echo 錯誤：git push 失敗，請確認網路或 GitHub 權限
  echo 按任何鍵離開...
  pause >nul
  exit /b 1
)

echo.
echo 完成！已上傳至 GitHub。
echo 按任何鍵離開...
pause >nul
