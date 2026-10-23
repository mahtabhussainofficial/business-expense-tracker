<div align="center">

  <h1>🏢 Multi-Tenant SaaS Business Expense Tracker</h1>
  <p><b>An enterprise-ready financial tracking and management web application built with Python and Flask.</b></p>

  <!-- Badges -->
  <p>
    <img src="https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
    <img src="https://img.shields.io/badge/Flask-Web%20Framework-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask" />
    <img src="https://img.shields.io/badge/Database-SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite" />
    <img src="https://img.shields.io/badge/Frontend-Chart.js-FF6384?style=for-the-badge&logo=chart.js&logoColor=white" alt="Chart.js" />
    <img src="https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge" alt="License" />
    <img src="https://img.shields.io/badge/Status-Production__Ready-brightgreen?style=for-the-badge" alt="Status" />
  </p>

  ---

</div>

<h2>📌 Table of Contents</h2>
<ul>
  <li><a href="#-about-the-project">About The Project</a></li>
  <li><a href="#-key-features">Key Features</a></li>
  <li><a href="#️-role-based-access-control-rbac">Role-Based Access Control (RBAC)</a></li>
  <li><a href="#️-tech-stack">Tech Stack</a></li>
  <li><a href="#-project-structure">Project Structure</a></li>
  <li><a href="#-getting-started--installation">Getting Started & Installation</a></li>
  <li><a href="#-security--smtp-alerts">Security & SMTP Alerts</a></li>
</ul>

<hr />

<h2 id="-about-the-project">📖 About The Project</h2>
<p>
  <b>Multi-Tenant SaaS Business Expense Tracker</b> ek advanced financial management solution hai jise specifically distinct organizations aur businesses ke liye design kiya gaya hai. Iska multi-tenant architecture ensure karta hai ke har company ka financial data mukammal tor par isolated aur secure rahe, jabke role-based permissions aur real-time visual analytics management ko behad asaan banate hain.
</p>

<hr />

<h2 id="-key-features">⚡ Key Features</h2>

<table>
  <tr>
    <th>Feature</th>
    <th>Description</th>
  </tr>
  <tr>
    <td><b>🏢 Multi-Tenant Architecture</b></td>
    <td>Complete data isolation per registered organization using relational foreign keys.</td>
  </tr>
  <tr>
    <td><b>📊 Visual Analytics</b></td>
    <td>Dynamic category-wise expense distribution powered by interactive <b>Chart.js</b> doughnut graphs.</td>
  </tr>
  <tr>
    <td><b>📥 Audit & Reporting</b></td>
    <td>On-the-fly CSV generation for tax, auditing, and accounting data downloads.</td>
  </tr>
  <tr>
    <td><b>🔒 Secure Authentication</b></td>
    <td>Session-based user sessions with salted SHA-256 password hashing via Werkzeug.</td>
  </tr>
  <tr>
    <td><b>📧 Automated Security Alerts</b></td>
    <td>Asynchronous background SMTP email dispatch notifying users upon successful account access.</td>
  </tr>
</table>

<hr />

<h2 id="️-role-based-access-control-rbac">👥 Role-Based Access Control (RBAC)</h2>

<table>
  <tr>
    <th>Role</th>
    <th>Permissions & Capabilities</th>
  </tr>
  <tr>
    <td><b>👑 Admin</b></td>
    <td>Add employees, delete all company transactions, perform bulk data resets, and export company audit reports.</td>
  </tr>
  <tr>
    <td><b>👤 Staff</b></td>
    <td>Log income/expenses and securely delete only self-created records.</td>
  </tr>
</table>

<hr />

<h2 id="️-tech-stack">🛠️ Tech Stack</h2>

<ul>
  <li><b>Backend:</b> Python 3, Flask, Jinja2 Templates</li>
  <li><b>Database & ORM:</b> SQLite, Flask-SQLAlchemy</li>
  <li><b>Frontend:</b> HTML5, Modern Responsive CSS3, Chart.js</li>
  <li><b>Security & Protocols:</b> Werkzeug (Security), smtplib (Threaded SMTP dispatch)</li>
  <li><b>Data Processing:</b> Python built-in <code>csv</code>, <code>io.StringIO</code>, <code>json</code></li>
</ul>

<hr />

<h2 id="-project-structure">📂 Project Structure</h2>

<pre><code>├── flask_app.py          # Application factory, routes, and database models
├── database.db           # SQLite database engine
├── templates/
│   ├── index.html        # Main dashboard with Chart.js analytics & controls
│   ├── login.html        # User login portal
│   ├── register.html     # Business tenant onboarding portal
│   └── add_staff.html    # Role-based employee creation form
└── README.md             # Project documentation</code></pre>

<hr />

<h2 id="-getting-started--installation">🚀 Getting Started & Installation</h2>

<h3>1. Clone the Repository</h3>
<pre><code>git clone https://github.com/mahtabhussainofficial/business-expense-tracker.git
cd business-expense-tracker</code></pre>

<h3>2. Install Dependencies</h3>
<pre><code>pip install flask flask-sqlalchemy werkzeug</code></pre>

<h3>3. Run the Application</h3>
<pre><code>python flask_app.py</code></pre>
<p>App locally <code>http://127.0.0.1:5000</code> par run ho jayegi.</p>

<hr />

<h2 id="-security--smtp-alerts">🛡️ Security & SMTP Alerts</h2>
<blockquote>
  <p><b>Note:</b> Make sure to configure your environment variables or config file for SMTP server credentials to enable background security login alerts seamlessly.</p>
</blockquote>

<hr />

<div align="center">
  <p>Crafted with ❤️ by <a href="https://github.com/mahtabhussainofficial"><b>Mahtab Hussain</b></a></p>
</div>
