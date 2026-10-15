# রঙতুলি স্টুডিও — Termux + GitHub + Android APK

এই প্যাকেজে আপনার আগের `rongtuli_studio_500` ওয়েব অ্যাপের মূল ফাইল রাখা হয়েছে। Android অ্যাপ তৈরির জন্য Capacitor কনফিগারেশন ও GitHub Actions workflow যোগ করা হয়েছে। ফোনে Android SDK/Gradle ইনস্টল না করেও GitHub-এর cloud runner-এ **debug APK** তৈরি করা যাবে।

## ১) ZIP Extract

Android-এর Files অ্যাপ দিয়ে ZIP-টি Extract করুন। Extract করা `rongtuli_studio_android_ready` ফোল্ডারটি ফোনের Downloads-এ রাখুন। Termux-এ:

```bash
pkg update -y
pkg install git unzip nodejs-lts -y
termux-setup-storage
cd ~/storage/downloads
ls
```

ফোল্ডারের নাম আলাদা হলে `cd`-তে আপনার আসল নাম ব্যবহার করুন। উদাহরণ:

```bash
cd ~/storage/downloads/rongtuli_studio_android_ready
```

যদি ফোল্ডার Downloads-এ না থাকে, আগে Files অ্যাপ দিয়ে সেখানে সরিয়ে নিন।

## ২) GitHub repository তৈরি

1. ব্রাউজারে https://github.com/new খুলুন এবং একটি নতুন repository তৈরি করুন, যেমন `rongtuli-studio`।
2. Public বা Private যেকোনোটি নিতে পারেন। README, .gitignore বা license আগে থেকে যোগ না করাই সহজ।
3. repository-র HTTPS URL কপি করুন। URL সাধারণত `https://github.com/USERNAME/rongtuli-studio.git`-এর মতো হবে।

## ৩) GitHub-এ push

প্রজেক্টের root ফোল্ডারে থেকে চালান:

```bash
git init
git branch -M main
git add .
git commit -m "Prepare Rongtuli Studio Android build"
git remote add origin https://github.com/USERNAME/rongtuli-studio.git
git push -u origin main
```

`USERNAME` এবং repository নাম আপনার নিজের তথ্য দিয়ে বদলাবেন। আগে থেকেই `origin` থাকলে `git remote set-url origin YOUR_REPOSITORY_URL` ব্যবহার করুন। GitHub authentication চাইলে আপনার GitHub sign-in/credential পদ্ধতি অনুসরণ করুন; account password সরাসরি Git prompt-এ কাজ নাও করতে পারে। Fine-grained Personal Access Token ব্যবহার করলে সেটি কাউকে দেবেন না এবং কোনো ফাইলে লিখে রাখবেন না।

বিকল্পভাবে `scripts/termux-push.sh` চালাতে পারেন:

```bash
bash scripts/termux-push.sh
```

## ৪) APK তৈরি — ফোনে SDK লাগবে না

1. GitHub repository খুলুন → **Actions**।
2. `Build Android APK` workflow-টি দেখুন। প্রথমবার Actions অনুমোদন করতে বললে অনুমোদন দিন।
3. `Build Android APK` নির্বাচন করে **Run workflow** চাপুন, অথবা `main`-এ push হওয়ার পর স্বয়ংক্রিয় build শেষ হতে দিন।
4. সবুজ সফল run খুলুন। নিচে **Artifacts** থেকে `rongtuli-studio-debug-apk` ডাউনলোড করুন।
5. ZIP artifact-টি Extract করুন; ভেতরের `app-debug.apk` ফোনে ইনস্টল করুন। Android অনুমতি চাইলে আপনার ব্রাউজার/ফাইল ম্যানেজারের জন্য “Install unknown apps” অনুমতি দিন। শুধু নিজের বিশ্বাসযোগ্য build ইনস্টল করুন।

## ৫) অ্যাপের ওয়েব ফাইল বদলালে

মূল ওয়েব ফাইল: `rongtuli_studio_500/index.html`। Android build-এ ব্যবহৃত কপি: `www/index.html`। পরিবর্তন করলে Termux-এ `bash scripts/sync-web-files.sh` চালিয়ে `www/` কপি আপডেট করুন। তারপর `git add .`, `git commit -m "Update app"`, `git push` করুন।

## কী আছে

- মূল রঙতুলি স্টুডিও HTML, README ও বাংলা পরিকল্পনার ফাইল
- PWA manifest এবং service worker
- Capacitor Android wrapper configuration
- GitHub Actions workflow: ক্লাউডে debug APK build ও artifact upload
- Termux push helper script ও web ফাইল sync script
- `.gitignore`

## গুরুত্বপূর্ণ সীমাবদ্ধতা

- এটি **debug APK**, Play Store-এ প্রকাশের জন্য signed release/AAB ও নিজস্ব signing key আলাদাভাবে সেট করতে হবে।
- GitHub Actions build চালাতে GitHub-এর usage limits ও repository permissions প্রযোজ্য।
- মূল অ্যাপটি single-file HTML; এই প্যাকেজে মূল UI নতুন করে লেখা হয়নি। Web app-এর কোনো ত্রুটি থাকলে সেটি আলাদাভাবে ঠিক করতে হবে।
- Android-এর native feature (যেমন push notification, billing বা file-system integration) নিজে থেকে যোগ হয় না; প্রয়োজন হলে আলাদা implementation লাগবে।
