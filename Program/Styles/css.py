CSS = {'MAIN':"""
/* ---------------------- Base Styles ---------------------- */
body {
    margin: 0;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background-color: #0d0f1a;
    background-image: radial-gradient(rgba(255,255,255,0.05) 1px, transparent 1px);
    background-size: 20px 20px;
    color: #EAECEF;
}

/* ---------------------- Scrollbar ---------------------- */
body::-webkit-scrollbar {
    width: 10px;
    height: 10px;
}
body::-webkit-scrollbar-track {
    background: #181A20;
    border-radius: 10px;
}
body::-webkit-scrollbar-thumb {
    background: #4aa96c;
    border-radius: 10px;
    border: 2px solid #181A20;
}
body::-webkit-scrollbar-thumb:hover {
    background: #66cc88;
}

/* ---------------------- Header ---------------------- */
header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20px 40px;
    background-color: #131722;
    border-bottom: 1px solid #222635;
}
header h2 {
    margin: 0;
    font-size: 24px;
    color: #4aa96c;
}
header h2[class="user-name"] {
    margin: 0;
    font-size: 24px;
    color: #eeeeee;
}
header p {
    margin: 0;
    font-size: 14px;
    color: #888;
}

/* ---------------------- Container ---------------------- */
.container {
    max-width: 1200px;
    margin: auto;
    padding: 20px 40px;
}

/* ---------------------- Card ---------------------- */
.card,
.trade-card,
.balance-card {
    background-color: #1b1f2a;
    border-radius: 10px;
    padding: 20px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.5);
    margin-bottom: 20px;
}
.trade-card {
    padding: 25px;
    border-radius: 12px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.6);
}
.card h2,
.trade-header h3,
.balance-card h3 {
    margin: 0;
    font-size: 18px;
    color: #4aa96c;
}
.balance-card {
    text-align: left;
    padding: 40px;
}
.balance-card .total {
    font-size: 30px;
    font-weight: bold;
    margin-bottom: 10px;
    color: #ffffff;
}
.balance-card .sub {
    font-size: 15px;
    color: #aaa;
    margin-bottom: 20px;
}
.balance-card .pie-chart {
    width: 100px;
    height: 100px;
    border-radius: 50%;
    background: conic-gradient(#4aa96c 0% 60%, #e74c3c 60% 100%);
}

/* ---------------------- Trade Header ---------------------- */
.trade-header {
    display: flex;
    align-items: center;
    gap: 15px;
    margin-bottom: 20px;
}
.trade-header img {
    width: 40px;
    height: 40px;
    border-radius: 50%;
}

/* ---------------------- Status ---------------------- */
.status {
    font-weight: bold;
    padding: 5px 12px;
    border-radius: 6px;
    font-size: 13px;
}
.closed { background: #143d2a; color: #4aa96c; }
.open { background: #3d1414; color: #e74c3c; }

/* ---------------------- Trade Info ---------------------- */
.trade-info {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 15px;
    margin-top: 15px;
}
.info-box {
    background: #0f131c;
    padding: 15px;
    border-radius: 8px;
}
.info-box h3 {
    margin: 0 0 5px 0;
    font-size: 14px;
    color: #aaa;
    font-weight: normal;
}
.info-box p {
    margin: 0;
    font-size: 16px;
    font-weight: bold;
    color: #fff;
}

/* ---------------------- Profit / Loss ---------------------- */
.profit { color: #4aa96c; font-weight: bold; }
.loss { color: #e74c3c; font-weight: bold; }

/* ---------------------- Table ---------------------- */
table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 10px;
    background-color: #1b1f2a;
    border-radius: 8px;
    overflow: hidden;
    cursor: pointer;
    font-size: 14px;
}
th {
    padding: 12px 8px;
    background-color: #131722;
    color: #aaa;
    font-weight: 600;
    border-bottom: 1px solid #222635;
    text-align: center;
}
td {
    padding: 10px 8px;
    text-align: center;
    border-bottom: 1px solid #222635;
    transition: background-color 0.2s ease, transform 0.1s ease;
}
tr:nth-child(even) {
    background-color: #181b26;
}
tr:hover {
    background-color: #222635;
}
.active-row:active {
    background-color: #acacac !important;
    box-shadow: inset 0 0 5px rgba(0,0,0,0.6);
}

/* ---------------------- Buttons ---------------------- */
button {
    background-color: #0b0d17;
    border: 1px solid #4aa96c;
    color: #4aa96c;
    padding: 5px 10px;
    border-radius: 5px;
    cursor: pointer;
}
button:hover {
    background-color: #4aa96c;
    color: #0b0d17;
}

/* ---------------------- Pairs List ---------------------- */
.pairs-list {
    display: flex;
    flex-direction: column;
    gap: 10px;
    margin-top: 10px;
}
.pairs-list .pair {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px 15px;
    background-color: #0f131c;
    border-radius: 6px;
    cursor: pointer;
    transition: background 0.2s;
    flex-wrap: wrap;
}
.pairs-list .pair:hover {
    background-color: #1e2433;
}
.pairs-list .left {
    display: flex;
    align-items: center;
    gap: 8px;
    min-width: 120px;
}
.pairs-list .middle {
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    min-width: 100px;
    margin-left: auto;
}
.pairs-list .icon {
    width: 22px;
    height: 22px;
    border-radius: 50%;
}
.pairs-list .symbol {
    font-weight: bold;
    color: #fff;
}
.price {
    color: #ddd;
    font-size: 14px;
}
.pairs-list .change {
    font-weight: bold;
    font-size: 13px;
}
.pairs-list .balances {
    display: flex;
    flex-direction: column;
    font-size: 12px;
    color: #bbb;
    min-width: 120px;
    margin-left: 20px;
}
.pairs-list .available { color: #4aa96c; }
.pairs-list .frozen { color: #e6c34a; }

/* ---------------------- Pair Cell ---------------------- */
.pair-cell {
    display: flex;
    align-items: center;
    gap: 8px;
}
.pair-cell img {
    width: 20px;
    height: 20px;
    border-radius: 50%;
}
       
/* ---------------------- Market Css ---------------------- */
.search-bar{
    margin-bottom:20px;
}

.search-bar input{
    width:100%;
    padding:10px;
    border-radius:8px;
    border:none;
}

.coins-grid{
    display:grid;
    grid-template-columns:repeat(auto-fill,minmax(180px,1fr));
    gap:15px;
}

.coin-card{
    background:#1e293b;
    padding:15px;
    border-radius:10px;
    cursor:pointer;
    position:relative;
    transition:0.2s;
}

.coin-card:hover{
    background:#334155;
}

.coin-name{
    font-size:18px;
    font-weight:bold;
}

.coin-price{
    margin-top:6px;
    font-size:14px;
}

.pen{
    position:absolute;
    right:10px;
    top:10px;
    cursor:pointer;
    font-size:14px;
    opacity:0.7;
}

.pen:hover{
    opacity:1;
}
       
/* --------- Coin Header --------------------- */

.coin-header{
display:flex;
align-items:center;
gap:15px;
}

.coin-icon{
width:48px;
height:48px;
border-radius:50%;
}

/* Pen Button */

.pen-btn{
width:42px;
height:42px;
border-radius:50%;
background:#4aa96c;
display:flex;
align-items:center;
justify-content:center;
font-size:20px;
cursor:pointer;
color:#0d0f1a;
border:none;
transition:0.2s;
}

.pen-btn:hover{
transform:scale(1.1);
background:#66cc88;
}
       
.login-btn{
height:42px;
padding-left:10px;
padding-right:10px;
border-radius:10px;
background:#4aa96c;
display:flex;
align-items:center;
justify-content:center;
font-size:20px;
cursor:pointer;
color:#0d0f1a;
border:none;
transition:0.2s;
}

.login-btn:hover{
transform:scale(1.1);
background:#66cc88;
}
"""}