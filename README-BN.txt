রঙতুলি Studio — GitHub-এ একবার Push করে Android APK Build

এই repository-তে মূল web app, Capacitor config, validation scripts এবং GitHub Actions workflow আছে। Android native project runner-এ স্বয়ংক্রিয়ভাবে তৈরি হবে।

একবারের সেটআপ
1. এই ZIP extract করুন। ZIP-এর ভেতরের সব ফাইল ও .github ফোল্ডার repository root-এ রাখুন।
2. GitHub-এ repository-তে commit/push করুন (যেকোনো branch-এ push হলেই workflow শুরু হবে)।
3. GitHub repository → Actions → সর্বশেষ “Build Rongtuli Android APK” run খুলুন।
4. সবুজ Success হলে নিচের Artifacts থেকে `rongtuli-studio-debug-apk` ডাউনলোড করুন। ZIP খুলে `app-debug.apk` ফোনে ইনস্টল করুন।

Workflow যা করে
- প্রয়োজনীয় ফাইল ও Capacitor config যাচাই করে
- inline JavaScript syntax পরীক্ষা করে
- Node.js 20 ও Java 21 ব্যবহার করে npm dependencies ইনস্টল করে
- Capacitor Android project তৈরি ও sync করে
- Gradle দিয়ে debug APK build করে
- APK artifact হিসেবে আপলোড করে

গুরুত্বপূর্ণ সীমাবদ্ধতা
- GitHub-এ push করার আগে repository-তে অন্য কোনো workflow বা আগের android/ folder থাকলে সেগুলো পরীক্ষা করুন; এই প্যাকেজে android/ ইচ্ছাকৃতভাবে নেই এবং runner-এ নতুন করে তৈরি হয়।
- সফল CI build মানে APK তৈরি হয়েছে; বাস্তব ফোনে সব feature-এর 100% কার্যকারিতা নিশ্চিত নয়। ফোনে install/run ও feature testing আলাদা ধাপ।
- Debug APK পরীক্ষামূলক ইনস্টলেশনের জন্য। Play Store প্রকাশের জন্য release signing key ও আলাদা signed release workflow দরকার।
- অ্যাপের HTML-এ যে lesson/content আছে শুধু সেটাই থাকবে; CI workflow নিজে নতুন ছবি, ভিডিও বা অডিও কনটেন্ট তৈরি করে না।
- Capacitor/Android tooling-এর নেটওয়ার্ক ও upstream পরিবর্তনের কারণে ভবিষ্যতে বিল্ড ব্যর্থ হতে পারে; তখন Actions log অনুযায়ী সংশোধন দরকার।

App ID: com.shikhiai.rongtulistudio
App name: Rongtuli Studio


Kotlin Duplicate class error fix (সংশোধিত)
- আগের ফিক্স সব Kotlin লাইব্রেরি জোর করে 1.8.22-এ নামিয়ে দিত; এটা নতুন AndroidX লাইব্রেরির সঙ্গে ঝুঁকিপূর্ণ ছিল।
- এখন scripts/patch-android.py শুধু kotlin-stdlib-jdk7 ও kotlin-stdlib-jdk8 কে 1.8.22-এ তোলে (এই দুটো 1.8.0 থেকে খালি forwarding লাইব্রেরি)। kotlin-stdlib নিজের স্বাভাবিক ভার্সনেই থাকে। এতে "Duplicate class kotlin.collections.jdk7/jdk8" এরর হয় না।
- একই স্ক্রিপ্ট AndroidManifest.xml-এ RECORD_AUDIO ও MODIFY_AUDIO_SETTINGS পারমিশন যোগ করে (অডিও রেকর্ডিংয়ের জন্য; আগে APK-তে রেকর্ডিং কাজ করত না)।

এই সংস্করণে যা ঠিক করা হয়েছে
- APK-তে PNG/JPG/SVG/প্রজেক্ট/অ্যানিমেশন সেভ আগে নীরবে ব্যর্থ হতো (Android WebView blob ডাউনলোড করে না)। এখন Capacitor Filesystem + Share প্লাগইনে ফাইল তৈরি হয়ে শেয়ার মেনু খোলে (Drive/Files/WhatsApp/Facebook ইত্যাদি)।
- Service Worker APK-তে পুরোনো ভার্সন আটকে রাখত; APK-তে এখন বন্ধ, ব্রাউজারে network-first।
- Drawing: শুরুতে ক্যানভাস স্বচ্ছ হয়ে যেত (PNG-তে স্বচ্ছ ব্যাকগ্রাউন্ড); Undo/Redo-র পরে ফ্রেম পুরোনো ছবি রাখত; Bucket Fill বড় ক্যানভাসে মেমরি ক্র্যাশ করতে পারত; অপ্রয়োজনীয় resize-এ ক্যানভাস রিসেট হতো।
- Animation: "Play once" শেষ ফ্রেম দেখাত না; Onion Skin শুধু নামেই ছিল (এখন সত্যিই আগের ফ্রেম হালকা দেখায়); ভিডিও এক্সপোর্টে FPS/hold সীমা ঠিক করা হয়েছে; ফ্রেম বদলালে Undo ইতিহাস মিশে যেত।
- Social Design: Select/Move বোতাম কাজ করত না (শুধু ডাবল-ট্যাপে নড়ত); ভিন্ন ফন্টে টেক্সট ধরা যেত না; এক্সপোর্ট করা ছবিতে সিলেকশন বক্স ও হ্যান্ডেল ছাপা হতো; Lock বোতামের লেখা মিলত না।
- Audio: রেকর্ড চলাকালে পাঠ বদলালে রেকর্ডিং ভুল পাঠে সেভ হতো।
- ছোটখাটো: নমুনা বর্ণ (Guide) পাঠ বদলালে আপডেট হতো না; TTS না থাকলে বার্তা; Android status bar/নেভিগেশন বারের safe-area padding।

যাচাই
- npm run check : কনফিগ, JS সিনট্যাক্স, HTML-এর সব element id, sw.js
- GitHub Actions workflow-এ এখন scripts/patch-android.py চলে এবং নিজেই ফলাফল যাচাই করে।
- এখানে (এই পরিবেশে) Android APK build করা যায়নি; নেটওয়ার্ক বন্ধ থাকায় Gradle/npm প্যাকেজ নামানো যায়নি। তাই চূড়ান্ত APK GitHub Actions-এ বানাতে হবে। ফোনে ইনস্টল করে মাইক্রোফোন ও সেভ/শেয়ার একবার পরীক্ষা করে নিন।

অ্যাপের নাম ও আইকন
- লঞ্চারে অ্যাপের নাম: Rongtuli (capacitor.config.json-এর appName)। App ID আগের মতোই (com.shikhiai.rongtulistudio), বদলানো হয়নি।
- resources/ ফোল্ডারে নতুন লঞ্চার আইকন (adaptive + legacy + round)। workflow-এ scripts/patch-android.py এগুলো Android প্রজেক্টে বসায়।
- store/ ফোল্ডারে Google Play-র জন্য 512×512 আইকন ও 1024×500 feature graphic।
- Play Store-এ বিক্রি/প্রকাশের জন্য signed release (AAB) বিল্ড লাগবে; এই workflow শুধু debug APK বানায়।
