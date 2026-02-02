# Hostinger Deployment Guide - Frontend

## 🎉 Build Complete!

Your frontend has been built successfully and is ready for Hostinger deployment!

**Build Location**: `frontend/dist/`

---

## 📦 What's in the Build?

```
frontend/dist/
├── index.html           (0.47 kB)
├── assets/
│   ├── index-*.css     (8.55 kB - Styles)
│   └── index-*.js      (200.15 kB - App logic)
└── vite.svg            (Icon)
```

**Total Size**: ~209 kB (gzipped: ~65 kB) - Super fast! ⚡

---

## 🚀 Deploy to Hostinger - Step by Step

### **Method 1: File Manager (Easiest)**

#### **Step 1: Login to Hostinger**
1. Go to https://hpanel.hostinger.com
2. Login to your account
3. Select your hosting plan

#### **Step 2: Open File Manager**
1. Click on **"File Manager"**
2. Navigate to `public_html` folder
3. Create a new folder (optional): `scraper` or use root

#### **Step 3: Upload Files**
1. Click **"Upload Files"**
2. Navigate to: `d:\yash\New folder\flipkart_scraper\frontend\dist\`
3. Select **ALL files** in the `dist` folder:
   - `index.html`
   - `assets` folder (with all contents)
   - `vite.svg`
4. Upload!

#### **Step 4: Extract (if zipped)**
If you uploaded as ZIP:
1. Right-click the ZIP file
2. Select **"Extract"**
3. Delete the ZIP file after extraction

#### **Step 5: Test Your Site**
Visit your domain:
```
https://yourdomain.com
```
or
```
https://yourdomain.com/scraper
```

---

### **Method 2: FTP Upload** (Recommended for Large Files)

#### **Step 1: Get FTP Credentials**
1. In Hostinger panel, go to **"FTP Accounts"**
2. Note down:
   - **FTP Host**: `ftp.yourdomain.com`
   - **Username**: Your FTP username
   - **Password**: Your FTP password
   - **Port**: `21`

#### **Step 2: Connect with FileZilla**
1. Download FileZilla: https://filezilla-project.org
2. Open FileZilla
3. Enter FTP credentials:
   - Host: `ftp.yourdomain.com`
   - Username: Your username
   - Password: Your password
   - Port: `21`
4. Click **"Quickconnect"**

#### **Step 3: Upload Files**
1. **Local site** (left): Navigate to `d:\yash\New folder\flipkart_scraper\frontend\dist\`
2. **Remote site** (right): Navigate to `public_html`
3. Select all files in `dist` folder
4. Drag and drop to upload

#### **Step 4: Verify Upload**
Check that these files are on the server:
```
public_html/
├── index.html
├── assets/
│   ├── index-*.css
│   └── index-*.js
└── vite.svg
```

---

### **Method 3: Git Deployment** (Advanced)

#### **Step 1: Enable Git in Hostinger**
1. Go to **"Advanced"** → **"Git"**
2. Click **"Create Repository"**

#### **Step 2: Clone Your Repo**
```bash
git clone https://github.com/niteshyadav7/web-scraping.git
cd web-scraping/frontend
npm install
npm run build
cp -r dist/* ~/public_html/
```

---

## ⚙️ Configuration

### **Update API URL (If Needed)**

If your Render backend URL is different, update it:

**File**: `frontend/src/App.jsx`

```javascript
const API_URL = 'https://YOUR-ACTUAL-RENDER-URL.onrender.com/api'
```

Then rebuild:
```powershell
cd frontend
npm run build
```

---

## 🔧 Hostinger-Specific Settings

### **1. Set Index File**
In Hostinger panel:
1. Go to **"Advanced"** → **"Indexes"**
2. Set default document: `index.html`

### **2. Enable HTTPS**
1. Go to **"SSL"** section
2. Enable **"Force HTTPS"**
3. Install free SSL certificate (Let's Encrypt)

### **3. Configure .htaccess** (For SPA Routing)

Create `.htaccess` in `public_html`:

```apache
<IfModule mod_rewrite.c>
  RewriteEngine On
  RewriteBase /
  RewriteRule ^index\.html$ - [L]
  RewriteCond %{REQUEST_FILENAME} !-f
  RewriteCond %{REQUEST_FILENAME} !-d
  RewriteRule . /index.html [L]
</IfModule>
```

This ensures the app works even with direct URL access.

---

## 🌐 Custom Domain Setup

### **If Using Subdomain**:
1. Go to **"Domains"** → **"Subdomains"**
2. Create subdomain: `scraper.yourdomain.com`
3. Point to folder: `public_html/scraper`
4. Upload files to that folder

### **If Using Main Domain**:
Upload directly to `public_html`

---

## ✅ Post-Deployment Checklist

After uploading, verify:

- [ ] `index.html` is in the root folder
- [ ] `assets` folder exists with CSS and JS files
- [ ] Site loads at your domain
- [ ] API calls work (check browser console)
- [ ] HTTPS is enabled
- [ ] No 404 errors

---

## 🐛 Troubleshooting

### **Issue 1: Blank Page**

**Solution**:
1. Check browser console (F12)
2. Look for errors
3. Verify API URL is correct
4. Check if files uploaded correctly

### **Issue 2: API Errors (CORS)**

**Solution**:
Your Render backend needs to allow your domain.

Update `api.py`:
```python
CORS(app, origins=['https://yourdomain.com'])
```

### **Issue 3: 404 on Refresh**

**Solution**:
Add `.htaccess` file (see above)

### **Issue 4: Files Not Found**

**Solution**:
1. Check file paths are correct
2. Ensure `assets` folder uploaded
3. Verify permissions (755 for folders, 644 for files)

---

## 📊 Performance Optimization

### **1. Enable Gzip Compression**

Add to `.htaccess`:
```apache
<IfModule mod_deflate.c>
  AddOutputFilterByType DEFLATE text/html text/css application/javascript
</IfModule>
```

### **2. Browser Caching**

Add to `.htaccess`:
```apache
<IfModule mod_expires.c>
  ExpiresActive On
  ExpiresByType text/css "access plus 1 year"
  ExpiresByType application/javascript "access plus 1 year"
</IfModule>
```

### **3. CDN (Optional)**

Use Cloudflare for free CDN:
1. Sign up at cloudflare.com
2. Add your domain
3. Update nameservers
4. Enable caching

---

## 🔄 Updating Your Site

When you make changes:

1. **Rebuild locally**:
   ```powershell
   cd frontend
   npm run build
   ```

2. **Upload new files**:
   - Delete old `assets` folder on server
   - Upload new `dist` contents

3. **Clear cache**:
   - Clear browser cache (Ctrl+Shift+R)
   - Or add version query: `?v=2`

---

## 📁 Recommended Folder Structure

```
public_html/
├── index.html              ← Your scraper app
├── assets/
│   ├── index-*.css
│   └── index-*.js
├── .htaccess              ← Routing rules
└── vite.svg
```

Or with subdomain:
```
public_html/
├── scraper/               ← Scraper app
│   ├── index.html
│   ├── assets/
│   └── .htaccess
└── index.html            ← Main site
```

---

## 🎯 Quick Upload Checklist

1. ✅ Build frontend (`npm run build`)
2. ✅ Login to Hostinger
3. ✅ Open File Manager
4. ✅ Navigate to `public_html`
5. ✅ Upload all files from `frontend/dist/`
6. ✅ Create `.htaccess` file
7. ✅ Enable HTTPS
8. ✅ Test your site!

---

## 🌟 Your Site is Live!

**Frontend**: `https://yourdomain.com`  
**Backend**: `https://flipkart-scraper-api.onrender.com`

**Test the scraper**:
1. Open your site
2. Enter a Flipkart URL
3. Set date range
4. Click "Start Scraping"
5. Watch the progress!

---

## 📞 Need Help?

**Common Issues**:
- Blank page → Check console for errors
- API errors → Verify Render backend URL
- 404 errors → Add `.htaccess` file
- Slow loading → Enable gzip compression

**Hostinger Support**:
- Live chat available 24/7
- Knowledge base: https://support.hostinger.com

---

**Your frontend is ready to deploy! 🚀**

**Build location**: `d:\yash\New folder\flipkart_scraper\frontend\dist\`
