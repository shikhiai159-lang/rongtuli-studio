#!/data/data/com.termux/files/usr/bin/bash
set -e
printf '\nরঙতুলি স্টুডিও — GitHub Push Helper\n'
printf 'এই স্ক্রিপ্ট চালানোর আগে ZIP extract করে সেই ফোল্ডারে Termux খুলুন।\n\n'
if ! command -v git >/dev/null 2>&1; then
  echo 'Git ইনস্টল নেই। চালান: pkg install git -y'; exit 1
fi
if [ ! -f package.json ] || [ ! -d www ]; then
  echo 'ভুল ফোল্ডার। package.json ও www ফোল্ডার আছে এমন প্রজেক্ট রুটে যান।'; exit 1
fi
if [ ! -d .git ]; then git init; fi
git branch -M main
git add .
printf '\nCommit message লিখুন (খালি রাখলে default হবে): '
read -r msg
msg=${msg:-"Prepare Rongtuli Studio Android build"}
if git diff --cached --quiet; then
  echo 'নতুন কোনো পরিবর্তন নেই।';
else
  git commit -m "$msg"
fi
printf '\nGitHub repository URL দিন (যেমন https://github.com/USERNAME/rongtuli-studio.git): '
read -r repo
if [ -z "$repo" ]; then echo 'Repository URL খালি রাখা যাবে না।'; exit 1; fi
if git remote get-url origin >/dev/null 2>&1; then git remote set-url origin "$repo"; else git remote add origin "$repo"; fi
git push -u origin main
printf '\nPush সম্পন্ন। GitHub repository → Actions-এ গিয়ে Build Android APK workflow দেখুন।\n'
