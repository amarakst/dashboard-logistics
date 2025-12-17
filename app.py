import streamlit as st
import pandas as pd
import plotly.express as px
import datetime
import time

def receive_3pl_update():
    """
    Simulasi data masuk dari sistem 3PL (API/Webhook).
    Data ini biasanya datang dalam format JSON.
    """
    update = {
        'ID_Pengiriman': 'SHP-002',
        'Status': 'Delayed',
        'Lat': -6.9175,
        'Lon': 107.6191,
        'Penyebab_Masalah': 'Macet Parah > 3 Jam'
    }
    return update

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="LogiSphere Control Tower", layout="wide", page_icon="🚚")

# --- DATA DUMMY (MENSIMULASIKAN DATABASE TERINTEGRASI) ---

def get_data():
    # Data Pesanan End-to-End (Order Status) - Menjawab Single Source of Truth
    order_data = pd.DataFrame({
        'ID_Pesanan': ['ORD-1001', 'ORD-1002', 'ORD-1003', 'ORD-1004'],
        'Distributor': ['Surabaya', 'Bandung', 'Semarang', 'Medan'],
        'Status_Hulu': ['RM Dipesan', 'RM Diterima', 'RM Diterima', 'RM Dipesan'], # Status Bahan Baku
        'Status_Pabrik': ['Belum Produksi', 'Sedang Produksi', 'Selesai Produksi', 'Belum Produksi'],
        'Status_Gudang': ['Menunggu', 'Menunggu', 'Siap Kirim', 'Menunggu'],
        'Status_Logistik': ['Menunggu', 'Delayed', 'Delivered', 'In Transit'], # Hubungan ke SHP-ID
        'ID_Pengiriman_Terkait': [None, 'SHP-002', 'SHP-003', 'SHP-004'],
        'Tanggal_Pesan': [datetime.date.today() - datetime.timedelta(days=7), datetime.date.today() - datetime.timedelta(days=5), datetime.date.today() - datetime.timedelta(days=10), datetime.date.today() - datetime.timedelta(days=4)],
    })
    
    # Data Stok Gudang (Warehouse)
    inventory_data = pd.DataFrame({
        'Kode_Barang': ['RM-001', 'RM-002', 'FG-101', 'FG-102'],
        'Nama_Barang': ['Tepung Terigu (Bahan Baku)', 'Gula Pasir (Bahan Baku)', 'Biskuit Coklat (Jadi)', 'Wafer Vanilla (Jadi)'],
        'Lokasi': ['Gudang A-1', 'Gudang A-2', 'Gudang B-1', 'Gudang B-2'],
        'Stok': [5000, 1200, 500, 8000],
        'Min_Stok': [1000, 1500, 1000, 2000],
        'Satuan': ['Kg', 'Kg', 'Karton', 'Karton']
    })
    
    # Data Pengiriman (Tracking) - Menjawab "Lubang Hitam" Logistik 
    shipment_data = pd.DataFrame({
        'ID_Pengiriman': ['SHP-001', 'SHP-002', 'SHP-003', 'SHP-004'],
        'Tujuan': ['Distributor Surabaya', 'Distributor Bandung', 'Distributor Semarang', 'Distributor Medan'],
        'Status': ['In Transit', 'Delayed', 'Delivered', 'In Transit'],
        'Ekspedisi_3PL': ['Logistik Cepat', 'Truk Nusantara', 'Cargo Kilat', 'Logistik Cepat'],
        'Sopir': ['Budi', 'Asep', 'Joko', 'Rian'],
        'Kontak_Sopir': ['0856-7788-9900', '0857-1122-3344', '0858-5566-7788', '0856-7788-9900'],
        'Kode_Tracking_Publik': ['LS-001X', 'LS-002Y', 'LS-003Z', 'LS-004A'],
        'ETA': [datetime.date.today(), datetime.date.today(), datetime.date.today() - datetime.timedelta(days=1), datetime.date.today() + datetime.timedelta(days=2)],
        'Lat': [-7.2575, -6.9175, -6.9667, 3.5952], # Koordinat dummy
        'Lon': [112.7521, 107.6191, 110.4167, 98.6722],
        'Penyebab_Masalah': [None, 'Macet > 2 Jam', None, None]
    })
    
    # Data Log Penanganan Pengecualian
    incident_data = pd.DataFrame({
        'ID_Insiden': ['INC-001'],
        'Tipe_Masalah': ['Pengiriman Terlambat'],
        'Terkait': ['SHP-002'],
        'Deskripsi_Masalah': ['Macet > 2 Jam di Tol Cipali'],
        'Tindakan_Korektif': ['Hubungi Sopir Asep, Alihkan ke Jalur Alternatif'],
        'Status': ['Selesai'],
        'Tanggal_Update': [datetime.datetime.now()]
    })
    update_baru = receive_3pl_update()
    mask = shipment_df['ID_Pengiriman'] == update_baru['ID_Pengiriman']
    shipment_df.loc[mask, 'Status'] = update_baru['Status']
    shipment_df.loc[mask, 'Lat'] = update_baru['Lat']
    shipment_df.loc[mask, 'Lon'] = update_baru['Lon']
    shipment_df.loc[mask, 'Penyebab_Masalah'] = update_baru['Penyebab_Masalah']
    
    return inventory_data, shipment_data, order_data, incident_data, shipment_df

inventory_df, shipment_df, order_df, incident_df = get_data()

# --- FUNGSI LOGIN ---
def login_page():
    st.markdown("<h1 style='text-align: center;'>LogiSphere - SCM Login</h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        if st.button("Login"):
            # Sederhana: hardcode untuk demo
            if username == "anya" and password == "admin123":
                st.session_state['logged_in'] = True
                st.session_state['role'] = 'Koordinator' # Anya adalah Koordinator [cite: 5]
                st.session_state['user'] = 'Anya Lestari'
                st.rerun()
            elif username == "gudang" and password == "gudang123":
                st.session_state['logged_in'] = True
                st.session_state['role'] = 'Staf Gudang'
                st.rerun()
            else:
                st.error("Username atau Password salah")

# --- DASHBOARD UTAMA (Mata Elang Anya) ---
def show_dashboard():
    st.title(f"👋 Selamat Datang, {st.session_state['user']}")
    st.markdown("### 🦅 End-to-End Supply Chain Overview")
    st.caption("Memantau aliran barang dari hulu ke hilir [cite: 12]")

    # 1. Metrics Utama
    col1, col2, col3, col4 = st.columns(4)
    
    total_active = len(shipment_df[shipment_df['Status'] == 'In Transit'])
    delayed = len(shipment_df[shipment_df['Status'] == 'Delayed'])
    low_stock_count = len(inventory_df[inventory_df['Stok'] < inventory_df['Min_Stok']])
    
    col1.metric("Pengiriman Aktif", f"{total_active} Truk", "Stabil")
    col2.metric("Pengiriman Tertunda", f"{delayed} Truk", "-1 (Bahaya)", delta_color="inverse")
    col3.metric("Alert Stok Menipis", f"{low_stock_count} Item", "Perlu Restock", delta_color="inverse")
    col4.metric("Lead Time Rata-rata", "3.2 Hari", "-0.5 Hari (Membaik)")

    st.divider()

    # 2. Peta Posisi & Grafik (Visibilitas Penuh )
    c1, c2 = st.columns([2, 1])
    
    with c1:
        st.subheader("📍 Peta Posisi Kendaraan (Real-time)")
        # Filter hanya yang aktif/delayed untuk peta
        active_ships = shipment_df[shipment_df['Status'].isin(['In Transit', 'Delayed'])]
        st.map(active_ships, latitude='Lat', longitude='Lon', size=20, color='#FF4B4B')
        st.caption("*Data posisi berdasarkan update terakhir GPS Mitra 3PL*")

    with c2:
        st.subheader("📊 Status Stok Gudang")
        # Visualisasi Stok vs Min Stok
        fig = px.bar(inventory_df, x='Kode_Barang', y=['Stok', 'Min_Stok'], barmode='group',
                     title="Stok vs Ambang Batas")
        st.plotly_chart(fig, use_container_width=True)

    # 3. Notifikasi Proaktif [cite: 20]
    st.subheader("⚠️ Peringatan Dini (Early Warning System)")
    if delayed > 0:
        for index, row in shipment_df[shipment_df['Status'] == 'Delayed'].iterrows():
            st.error(f"ALERT: Pengiriman {row['ID_Pengiriman']} ke {row['Tujuan']} TERLAMBAT. Penyebab: {row['Penyebab_Masalah']}")
    
    if low_stock_count > 0:
        for index, row in inventory_df[inventory_df['Stok'] < inventory_df['Min_Stok']].iterrows():
            st.warning(f"ALERT: Stok {row['Nama_Barang']} ({row['Stok']} {row['Satuan']}) di bawah batas aman!")
            
# --- TRACKING PUBLIK UNTUK PELANGGAN ---
def show_public_tracking():
    st.title("📦 Pelacakan Pesanan Anda")
    st.subheader("LogiSpehere - Customer Tracking")
    
    # Form input untuk Kode Pelacakan
    tracking_code = st.text_input("Masukkan Kode Pelacakan (Contoh: LS-001X)", "")
    
    if tracking_code:
        # Cari data berdasarkan Kode Pelacakan Publik
        result_df = shipment_df[shipment_df['Kode_Tracking_Publik'] == tracking_code.upper().strip()]
        
        if not result_df.empty:
            detail = result_df.iloc[0]
            
            st.success(f"Status Ditemukan untuk Pesanan Tujuan: **{detail['Tujuan']}**")
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Status Terkini", detail['Status'])
            col2.metric("Estimasi Waktu Tiba (ETA)", detail['ETA'].strftime('%d %B %Y'))
            col3.metric("Ekspedisi", detail['Ekspedisi_3PL'])
            
            st.divider()
            
            # Tampilkan Peta Sederhana (Jika posisi tersedia)
            st.subheader("Lokasi Terakhir Kendaraan")
            
            # Filter hanya koordinat yang ditemukan
            map_data = result_df[['Lat', 'Lon']].dropna()
            if not map_data.empty:
                st.map(map_data, latitude='Lat', longitude='Lon', zoom=6)
                st.caption("*Data lokasi diperbarui secara real-time.*")
            else:
                 st.info("Informasi lokasi detail belum tersedia.")

            # Berikan informasi kontak tim Sales/CS jika ada masalah
            st.markdown("---")
            st.markdown("Jika ada pertanyaan lebih lanjut, silakan hubungi tim Customer Service kami (+6285156749374).")
            
        else:
            st.error(f"Kode pelacakan **{tracking_code}** tidak ditemukan atau tidak valid.")
# --- WAREHOUSE MANAGEMENT ---
def show_warehouse():
    st.title("🏭 Warehouse Management")
    st.markdown("Mengelola stok bahan baku dan barang jadi.")

    # Pencarian Cepat
    search = st.text_input("🔍 Cari Kode Barang / Nama Barang", "")
    
    # Filter Data
    if search:
        filtered_df = inventory_df[inventory_df['Nama_Barang'].str.contains(search, case=False) | inventory_df['Kode_Barang'].str.contains(search, case=False)]
    else:
        filtered_df = inventory_df

    # Tampilan Tabel dengan Formatting Kondisional
    def highlight_stock(val):
        # Logika sederhana untuk simulasi warna
        if isinstance(val, int) and val < 1000:
            return 'background-color: #ffcccc' # Merah muda jika stok rendah
        return ''

    st.dataframe(filtered_df.style.applymap(highlight_stock, subset=['Stok']), use_container_width=True)

    # Form Mutasi Stok Sederhana
    st.divider()
    st.subheader("📝 Input Mutasi Stok (Masuk/Keluar)")
    c1, c2, c3 = st.columns(3)
    c1.selectbox("Pilih Barang", inventory_df['Kode_Barang'])
    c2.number_input("Jumlah", min_value=1)
    c3.selectbox("Tipe Mutasi", ["Barang Masuk (Inbound)", "Barang Keluar (Outbound)"])
    if st.button("Simpan Mutasi"):
        st.success("Data mutasi berhasil disimpan!")

# --- TRACKING PENGIRIMAN ---
def show_tracking():
    st.title("🚚 End-to-End Tracking")
    st.markdown("Memantau pergerakan barang dari pabrik ke distributor.")

    # Filter Status
    status_filter = st.multiselect("Filter Status:", options=shipment_df['Status'].unique(), default=['In Transit', 'Delayed'])
    
    filtered_ships = shipment_df[shipment_df['Status'].isin(status_filter)]
    
    st.dataframe(filtered_ships, use_container_width=True)

    # Detail Pelacakan (Menghapus 'Lubang Hitam' 3PL )
    st.subheader("Detail Perjalanan")
    selected_id = st.selectbox("Pilih ID Pengiriman untuk Detail:", filtered_ships['ID_Pengiriman'])
    
    if selected_id:
        detail = shipment_df[shipment_df['ID_Pengiriman'] == selected_id].iloc[0]
        st.info(f"**Ekspedisi (3PL):** {detail['Ekspedisi_3PL']} | **Sopir:** {detail['Sopir']}")
        st.write(f"**Estimasi Tiba (ETA):** {detail['ETA']}")
        
        # Simulasi Google Maps Link (Integration Mockup)
        maps_url = f"https://www.google.com/maps/search/?api=1&query={detail['Lat']},{detail['Lon']}"
        st.markdown(f"[➡️ Lihat Lokasi Truk di Google Maps]({maps_url})")

# --- LAPORAN KERJA ---
def show_reports():
    st.title("📈 Laporan & Analisa")
    st.markdown("Mengidentifikasi bottleneck dan mengukur performa[cite: 22].")
    
    tab1, tab2, tab3 = st.tabs(["Performa Pengiriman", "Akar Masalah Keterlambatan", "Analisa Lead Time"]) 

    with tab1:
        # Grafik Pie Chart Status Pengiriman
        fig_pie = px.pie(shipment_df, names='Status', title='Persentase Status Pengiriman')
        st.plotly_chart(fig_pie)
        
        # Grafik Volume (Dummy Trend)
        dates = pd.date_range(start='2023-10-01', periods=30)
        volume = [x * 10 + (x%5)*20 for x in range(30)] # Data dummy
        df_trend = pd.DataFrame({'Tanggal': dates, 'Volume': volume})
        fig_line = px.line(df_trend, x='Tanggal', y='Volume', title='Tren Volume Pengiriman Bulan Ini')
        st.plotly_chart(fig_line)

    with tab2:
        # Analisa Akar Masalah [cite: 36]
        problems = {'Macet': 12, 'Produksi Telat': 5, 'Masalah Dokumen': 3, 'Kendala Kendaraan': 8}
        df_prob = pd.DataFrame(list(problems.items()), columns=['Penyebab', 'Jumlah Kasus'])
        fig_bar = px.bar(df_prob, x='Penyebab', y='Jumlah Kasus', title='Penyebab Keterlambatan Terbanyak', color='Penyebab')
        st.plotly_chart(fig_bar)
    with tab3: # Tab baru
        st.subheader("Analisa Lead Time Berdasarkan Tahap")
        # Data dummy untuk Lead Time Tahapan
        lead_time_data = pd.DataFrame({
            'Tahap': ['Order to Produce', 'Produce to Warehouse', 'Warehouse to Customer'],
            'Waktu_Rata2_Hari': [1.5, 1.0, 2.7],
            'Benchmark_Hari': [1.0, 0.5, 2.0]
        })
        fig_lt = px.bar(lead_time_data, x='Tahap', y=['Waktu_Rata2_Hari', 'Benchmark_Hari'], 
                         barmode='group', title='Lead Time vs Target per Tahap',
                         labels={'value': 'Waktu (Hari)', 'variable': 'Metrik'})
        st.plotly_chart(fig_lt, use_container_width=True)
        
        st.caption("Visualisasi ini membantu mengidentifikasi 'Warehouse to Customer' sebagai **bottleneck** terbesar.")

    # Fitur Ekspor
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            label="📥 Download Laporan (Excel)",
            data=shipment_df.to_csv().encode('utf-8'),
            file_name='laporan_pengiriman.csv',
            mime='text/csv',
        )

# --- SUPPLIER & DISTRIBUTOR SCORECARD ---
def show_partners():
    st.title("🤝 Manajemen Mitra (3PL & Distributor)")
    st.markdown("Penilaian performa untuk meningkatkan akurasi janji pengiriman[cite: 23].")

    partners = pd.DataFrame({
        'Nama Mitra': ['Logistik Cepat', 'Truk Nusantara', 'Cargo Kilat'],
        'Tipe': ['3PL', '3PL', '3PL'],
        'Total Pengiriman': [150, 120, 200],
        'Tepat Waktu (%)': [95, 80, 88],
        'Rating': ['⭐⭐⭐⭐⭐', '⭐⭐⭐', '⭐⭐⭐⭐'],
        'Kontak_3PL': ['0811-2233-4455', '0812-3456-7890', '0813-9876-5432']
    })
    
    st.table(partners)
    
# --- ORDER STATUS END-TO-END ---
def show_order_status():
    st.title("📦 Order Status End-to-End")
    st.markdown("Visibilitas status pesanan dari Bahan Baku hingga Pengiriman.")
    
    # Filter dan Pencarian
    col1, col2 = st.columns(2)
    search_order = col1.text_input("🔍 Cari ID Pesanan/Distributor", "")
    status_filter = col2.multiselect("Filter Status Logistik:", options=order_df['Status_Logistik'].unique(), default=order_df['Status_Logistik'].unique())
    
    filtered_orders = order_df[order_df['Status_Logistik'].isin(status_filter)]
    if search_order:
        filtered_orders = filtered_orders[filtered_orders['Distributor'].str.contains(search_order, case=False) | filtered_orders['ID_Pesanan'].str.contains(search_order, case=False)]
        
    st.dataframe(filtered_orders, use_container_width=True)
    
    # Visualisasi Rantai Pasok (Simulasi Aliran)     st.subheader("Visualisasi Aliran Status Rantai Pasok")
    # Tampilkan Flow Chart/Diagram Status
    # Contoh visualisasi sederhana:
    status_counts = filtered_orders['Status_Logistik'].value_counts().reset_index()
    status_counts.columns = ['Status', 'Jumlah']
    fig = px.sunburst(
        filtered_orders, 
        path=['Status_Hulu', 'Status_Pabrik', 'Status_Gudang', 'Status_Logistik'], 
        title='Aliran Status E2E (Sunburst Chart)'
    )
    st.plotly_chart(fig, use_container_width=True)

    st.caption("Memvisualisasikan 4 tahapan utama: Hulu (Bahan Baku), Pabrik (Produksi), Gudang, dan Logistik.")

# --- MANAJEMEN INSIDEN/PENGECUALIAN ---
def show_incidents():
    st.title("🚨 Manajemen Insiden Proaktif")
    st.markdown("Mencatat dan menindaklanjuti peringatan dini.")
    
    st.subheader("Log Insiden Aktif & Riwayat")
    
    # Tampilan Log
    st.dataframe(incident_df, use_container_width=True)
    
    st.divider()
    
    # Form Input Tindak Lanjut
    st.subheader("Tambahkan Tindakan Korektif Baru")
    
    with st.form("incident_form"):
        col1, col2 = st.columns(2)
        
        related_id = col1.selectbox("Terkait Pengiriman (SHP-ID)", shipment_df['ID_Pengiriman'])
        problem_type = col2.selectbox("Tipe Masalah", ['Pengiriman Terlambat', 'Stok Tidak Cukup', 'Kualitas Bahan Baku'])
        
        description = st.text_area("Deskripsi Masalah")
        action = st.text_area("Tindakan Korektif yang Diambil")
        
        status = st.radio("Status Penanganan", ['Baru', 'Dalam Proses', 'Selesai'])
        
        if st.form_submit_button("Simpan Insiden & Tindakan"):
            # Simulasi penambahan data baru
            new_id = f"INC-{len(incident_df) + 1:03d}"
            new_row = pd.DataFrame([{
                'ID_Insiden': new_id,
                'Tipe_Masalah': problem_type,
                'Terkait': related_id,
                'Deskripsi_Masalah': description,
                'Tindakan_Korektif': action,
                'Status': status,
                'Tanggal_Update': datetime.datetime.now()
            }])
            # Di aplikasi nyata, ini akan memperbarui database
            # incident_df = pd.concat([incident_df, new_row], ignore_index=True)
            st.success(f"Insiden {new_id} berhasil dicatat dengan tindakan korektif!")
            
# --- LOGIC UTAMA APLIKASI ---
def main():
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
        st.session_state['public_mode'] = False

    if not st.session_state['logged_in']:
        st.sidebar.title("Akses Portal")
        mode = st.sidebar.radio("Pilih Akses:", ["Login Internal", "Customer Tracking"])
        if mode == "Login Internal":
            st.session_state['public_mode'] = False
            login_page()
        else:
            st.session_state['public_mode'] = True
            show_public_tracking()
    else:
        # Sidebar Menu
        with st.sidebar:
            st.image("https://cdn-icons-png.flaticon.com/512/4129/4129437.png", width=100)
            st.title("LogiSphere")
            st.write(f"Role: **{st.session_state['role']}**")
            st.divider()
            if st.button("🔄 Sinkronisasi Data 3PL"):
                with st.spinner('Mengambil data GPS...'):
                    time.sleep(1) # Simulasi loading API
                    st.rerun() # Memaksa aplikasi menjalankan ulang get_data()
            st.divider()
            
            menu = st.radio("Menu Navigasi", ["Dashboard Utama", "Order Status", "Warehouse", "Tracking Pengiriman", "Laporan Kerja", "Mitra & Supplier", "Manajemen Insiden"])
        
            st.divider()
            if st.button("Logout"):
                st.session_state['logged_in'] = False
                st.rerun()

        # Routing Halaman
        if menu == "Dashboard Utama":
            show_dashboard()
        elif menu == "Order Status":
            show_order_status()
        elif menu == "Warehouse":
            show_warehouse()
        elif menu == "Tracking Pengiriman":
            show_tracking()
        elif menu == "Laporan Kerja":
            show_reports()
        elif menu == "Mitra & Supplier":
            show_partners()
        elif menu == "Manajemen Insiden": # Tambahan
            show_incidents()

if __name__ == "__main__":

    main()














