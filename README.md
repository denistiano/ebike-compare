# 🚴‍♂️ E-Bike Compare

**The most comprehensive e-bike comparison tool with automated data collection and GitHub Pages hosting.**

[![Deploy to GitHub Pages](https://github.com/your-username/ebike-compare/actions/workflows/deploy-site.yml/badge.svg)](https://github.com/your-username/ebike-compare/actions/workflows/deploy-site.yml)
[![Crawl E-Bike Sites](https://github.com/your-username/ebike-compare/actions/workflows/crawl-sites.yml/badge.svg)](https://github.com/your-username/ebike-compare/actions/workflows/crawl-sites.yml)

## 🎯 What is E-Bike Compare?

E-Bike Compare is a **modern, fully automated** e-bike comparison platform that:

- 📊 **Compares 100+ e-bikes** from major manufacturers
- 💰 **Tracks real-time pricing** and specifications
- 🤖 **Auto-updates daily** via GitHub Actions
- 🌐 **Hosted on GitHub Pages** - completely free
- 📱 **Mobile-responsive** design
- ⚡ **Lightning-fast** static site performance

## 🏗️ **NEW MODERNIZED ARCHITECTURE**

This project has been **completely restructured** from a Python Flask app to a modern static site with automated crawling:

### **Before (Old)**
```
❌ Python Flask server required
❌ Manual server maintenance  
❌ Mixed file structure
❌ Local hosting only
```

### **After (New)**
```
✅ Pure static HTML/CSS/JavaScript
✅ GitHub Actions for automation
✅ Clean, separated architecture
✅ GitHub Pages hosting
✅ Zero maintenance required
```

## 📁 Project Structure

```
📦 ebike-compare/
├── 🤖 .github/workflows/          # Automation
│   ├── crawl-sites.yml           # Daily data collection
│   └── deploy-site.yml           # Site deployment
├── 📊 src/                       # Source code
│   ├── crawlers/                 # Python crawlers
│   │   ├── crawler.py           # Main crawler logic
│   │   └── config/websites.py   # Site configurations
│   └── web/                     # Static website
│       ├── index.html           # Homepage
│       ├── compare.html         # Comparison tool
│       ├── css/main.css         # Styling
│       ├── js/                  # JavaScript apps
│       └── data/                # CSV data files
├── �� docs/                     # GitHub Pages output
├── 🔧 scripts/build.py          # Build automation
├── 📂 data/                     # Raw data storage
│   ├── current/                 # Latest data
│   └── archive/                 # Historical data
└── 📋 requirements.txt          # Python dependencies
```

## 🚀 How It Works

### **1. Automated Data Collection**
- **Daily at 6 AM UTC**: Crawlers run automatically
- **7 major manufacturers**: Trek, Specialized, Cube, Engwe, Fiido, Lectric, Rad Power
- **Smart extraction**: Prices, specs, images, URLs
- **Auto-archival**: Historical data preserved

### **2. Static Site Generation**
- **Build script** copies web files to `docs/`
- **GitHub Pages** serves from `docs/` directory
- **Instant deployment** on every update

### **3. Client-Side Magic**
- **CSV Parser**: Reads data files directly in browser
- **Dynamic Filtering**: Real-time search and sort
- **Responsive Design**: Perfect on all devices
- **No Server Required**: 100% client-side rendering

## 🎮 Usage

### **For Users (Website)**
1. **Browse**: View all available e-bikes with filters
2. **Compare**: Select bikes for side-by-side comparison
3. **Explore**: Click through to manufacturer websites

### **For Developers**

#### **Local Development**
```bash
# Serve the static site locally
cd src/web
python -m http.server 8000
# Visit http://localhost:8000
```

#### **Add New Manufacturers**
1. Edit `src/crawlers/config/websites.py`
2. Add website configuration with selectors
3. Test with: `python -m src.crawlers.crawler`

#### **Deploy Changes**
```bash
# Build and test
python scripts/build.py

# Commit and push
git add .
git commit -m "Update site"
git push  # Auto-deploys via GitHub Actions
```

## 🤖 GitHub Actions Workflows

### **Crawl Sites** (`crawl-sites.yml`)
- **Schedule**: Daily at 6 AM UTC
- **Trigger**: Manual dispatch available
- **Function**: Updates CSV data files
- **Auto-commit**: Pushes new data back to repo

### **Deploy Site** (`deploy-site.yml`)
- **Trigger**: Push to main branch
- **Function**: Builds and deploys to GitHub Pages
- **Path**: Monitors `src/web/` changes

## 📊 Data Sources

| Manufacturer | Region | Products | Status |
|-------------|--------|----------|---------|
| Trek | International | ~50 | ✅ Active |
| Specialized | USA | ~40 | ✅ Active |
| Cube Bikes | Germany | ~60 | ✅ Active |
| Engwe | US/EU | ~30 | ✅ Active |
| Fiido | Global | ~25 | ✅ Active |
| Lectric | USA | ~15 | ✅ Active |
| Rad Power | USA | ~20 | ✅ Active |

## 🛠️ Technical Stack

### **Frontend**
- **HTML5** + **CSS3** + **Vanilla JavaScript**
- **Bootstrap 5** for responsive UI
- **Custom CSV parser** for data loading
- **Client-side rendering** for speed

### **Backend** (GitHub Actions)
- **Python 3.11** with BeautifulSoup & pandas
- **Scheduled workflows** for automation
- **CSV data persistence**
- **Git-based deployment**

### **Hosting**
- **GitHub Pages** (free tier)
- **Custom domain** support ready
- **SSL/HTTPS** included
- **Global CDN** via GitHub

## 🎨 Features

### **🔍 Advanced Filtering**
- Filter by manufacturer, price range
- Real-time text search
- Sort by name, price, brand
- Results pagination

### **📊 Smart Comparison**
- Select up to 4 bikes
- Side-by-side specifications
- Highlighted differences
- Direct links to purchase

### **📱 Mobile-First Design**
- Responsive grid layout
- Touch-friendly interactions
- Fast loading on mobile
- Progressive enhancement

## 🚀 Deployment

### **Setup GitHub Pages**
1. Fork this repository
2. Go to Settings → Pages
3. Set source to "GitHub Actions"
4. Enable workflows in Actions tab

### **Custom Domain** (Optional)
1. Add `CNAME` file in `docs/`
2. Configure DNS records
3. Enable in GitHub Pages settings

## 🤝 Contributing

### **Add New Data Sources**
1. Research e-bike manufacturer website
2. Identify product listing and detail pages
3. Create selectors configuration
4. Test crawler with new config
5. Submit pull request

### **Improve Website**
1. Edit files in `src/web/`
2. Test locally with `python -m http.server`
3. Build with `python scripts/build.py`
4. Commit and push for auto-deployment

## 📈 Performance

- ⚡ **Sub-second load times** (static hosting)
- 📱 **Mobile-optimized** rendering
- 🔄 **Efficient data loading** (CSV parsing)
- 🎯 **SEO-friendly** structure
- 💾 **Minimal bandwidth** usage

## 📄 License

MIT License - Feel free to use and modify!

## 🤖 Automation Status

The following processes run automatically:

- ✅ **Daily data crawling** at 6 AM UTC
- ✅ **Automatic site deployment** on code changes  
- ✅ **Data archival** and version control
- ✅ **Error handling** and retry logic

---

**🌟 Star this repo if you find it useful!**

Built with ❤️ for the e-bike community.
