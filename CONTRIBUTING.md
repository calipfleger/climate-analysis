# 🌍 Climate Analysis - Contribution Guide  

## ✅ Git Workflow  
1. **Clone the repo**  
   ```bash
   git clone https://github.com/your-lab/climate-analysis.git

git checkout -b feature-branch-name


🔥 [MODULE] Short description of change  
Example: 🖼️ [PLOTTING] Fixed colormap issue for pcolormesh  


git push origin feature-branch-name

📌 **Then save & exit:** Press `CTRL + X`, then `Y`, then `Enter`.  

---

## 🔥 **Step 2: Automate Tests Using `pytest`**  
✅ **Why?** Catch errors **before** running full analysis, ensuring code stability.  

### **📌 Terminal Commands:**  
```bash
cd climate-analysis/src  # Go to the source directory
mkdir tests  # Create a folder for tests
nano tests/test_trend_analysis.py  # Create a test file for trend analysis

