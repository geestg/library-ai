import React from 'react';
import { 
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell, 
  PieChart, Pie 
} from 'recharts';
import { Users, Calendar, Award, Clock, Download, X, TrendingUp, BookOpen } from 'lucide-react';
import './VisitorDashboardModal.css';

const COLORS = ['#38bdf8', '#818cf8', '#34d399', '#fbbf24', '#f87171'];

export default function VisitorDashboardModal({ isOpen, onClose, data }) {
  if (!isOpen || !data) return null;

  const {
    monthLabel = "Semester Genap 2026",
    totalVisits = 0,
    avgDailyStr = "N/A",
    prodiData = [],
    slotData = [],
    topVisitors = [],
    downloadUrl = "",
    recommendations = []
  } = data;

  return (
    <div className="visitor-modal-overlay">
      <div className="visitor-modal-container">
        {/* Header */}
        <div className="visitor-modal-header">
          <div className="header-title-group">
            <div className="header-icon-badge">
              <Users size={24} className="text-sky-400" />
            </div>
            <div>
              <h2>Dashboard Analisis Pengunjung</h2>
              <p>Statistik & Pola Kunjungan Perpustakaan IT Del - {monthLabel}</p>
            </div>
          </div>
          <button onClick={onClose} className="close-btn" aria-label="Tutup Modal">
            <X size={20} />
          </button>
        </div>

        {/* Metric Cards */}
        <div className="metrics-grid">
          <div className="metric-card cyan">
            <div className="metric-header">
              <span className="metric-title">Total Kunjungan</span>
              <Users size={18} className="metric-icon text-sky-400" />
            </div>
            <div className="metric-value">{totalVisits.toLocaleString()}</div>
            <span className="metric-subtext">Pengunjung Tercatat</span>
          </div>

          <div className="metric-card emerald">
            <div className="metric-header">
              <span className="metric-title">Rata-rata Harian</span>
              <Calendar size={18} className="metric-icon text-emerald-400" />
            </div>
            <div className="metric-value">{avgDailyStr}</div>
            <span className="metric-subtext">Kunjungan per Hari</span>
          </div>

          <div className="metric-card indigo">
            <div className="metric-header">
              <span className="metric-title">Prodi Teraktif</span>
              <Award size={18} className="metric-icon text-indigo-400" />
            </div>
            <div className="metric-value">{prodiData[0]?.name || 'N/A'}</div>
            <span className="metric-subtext">Dominasi Kunjungan</span>
          </div>
        </div>

        {/* Charts Grid */}
        <div className="charts-grid">
          {/* Bar Chart - Prodi Teraktif */}
          <div className="chart-card">
            <div className="chart-header">
              <TrendingUp size={18} className="text-sky-400" />
              <h3>Top 5 Program Studi Teraktif</h3>
            </div>
            <div className="chart-body">
              <ResponsiveContainer width="100%" height={220}>
                <BarChart data={prodiData} layout="vertical" margin={{ top: 5, right: 20, left: 40, bottom: 5 }}>
                  <XAxis type="number" stroke="#94a3b8" />
                  <YAxis dataKey="name" type="category" stroke="#94a3b8" tick={{ fontSize: 11 }} width={120} />
                  <Tooltip 
                    contentStyle={{ backgroundColor: '#1e293b', borderColor: '#334155', borderRadius: '8px', color: '#f8fafc' }} 
                  />
                  <Bar dataKey="value" radius={[0, 6, 6, 0]}>
                    {prodiData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Pie Chart - Slot Waktu */}
          <div className="chart-card">
            <div className="chart-header">
              <Clock size={18} className="text-indigo-400" />
              <h3>Distribusi Slot Waktu Kunjungan</h3>
            </div>
            <div className="chart-body">
              <ResponsiveContainer width="100%" height={220}>
                <PieChart>
                  <Pie
                    data={slotData}
                    cx="50%"
                    cy="50%"
                    innerRadius={50}
                    outerRadius={80}
                    paddingAngle={4}
                    dataKey="value"
                  >
                    {slotData.map((entry, index) => (
                      <Cell key={`cell-slot-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip 
                    contentStyle={{ backgroundColor: '#1e293b', borderColor: '#334155', borderRadius: '8px', color: '#f8fafc' }} 
                  />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>

        {/* Top Visitors Table */}
        <div className="table-card">
          <div className="table-header">
            <Award size={18} className="text-yellow-400" />
            <h3>Top 5 Pengunjung Terloyal Perpustakaan</h3>
          </div>
          <div className="table-responsive">
            <table>
              <thead>
                <tr>
                  <th>NIM / No Anggota</th>
                  <th>Nama Lengkap</th>
                  <th>Program Studi</th>
                  <th>Total Kunjungan</th>
                </tr>
              </thead>
              <tbody>
                {topVisitors.map((v, i) => (
                  <tr key={i}>
                    <td className="font-mono text-sky-400">{v.nim}</td>
                    <td>{v.name}</td>
                    <td>{v.prodi}</td>
                    <td className="font-bold text-sky-400">{v.visits} kali</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Footer Actions */}
        <div className="modal-footer">
          {downloadUrl && (
            <a href={downloadUrl} target="_blank" rel="noreferrer" className="download-btn">
              <Download size={16} /> Unduh Rekap Excel (.xlsx)
            </a>
          )}
          <button onClick={onClose} className="close-action-btn">
            Tutup Dashboard
          </button>
        </div>
      </div>
    </div>
  );
}
