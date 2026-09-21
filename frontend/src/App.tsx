const stats = [
    { label: 'Protected files', value: '842' },
    { label: 'Threats found', value: '17' },
    { label: 'Avg scan', value: '112ms' },
    { label: 'System health', value: 'Healthy' },
];

export default function App() {
    return (
        <main style={{ fontFamily: 'Inter, sans-serif', background: '#0b1220', color: '#e5e7eb', minHeight: '100vh', padding: '32px' }}>
            <div style={{ maxWidth: 1100, margin: '0 auto' }}>
                <header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 32 }}>
                    <div>
                        <div style={{ fontSize: 12, letterSpacing: '0.12em', textTransform: 'uppercase', color: '#94a3b8' }}>ClamSentinel</div>
                        <h1 style={{ margin: '8px 0 0', fontSize: 32 }}>Operations Dashboard</h1>
                    </div>
                    <div style={{ padding: '10px 16px', borderRadius: 8, background: '#111827', border: '1px solid #374151' }}>
                        Status: Healthy
                    </div>
                </header>

                <section style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: 16, marginBottom: 32 }}>
                    {stats.map((stat) => (
                        <div key={stat.label} style={{ background: '#111827', border: '1px solid #374151', borderRadius: 12, padding: 20 }}>
                            <div style={{ color: '#94a3b8', fontSize: 12, marginBottom: 8 }}>{stat.label}</div>
                            <div style={{ fontSize: 28, fontWeight: 700 }}>{stat.value}</div>
                        </div>
                    ))}
                </section>

                <section style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: 16 }}>
                    <div style={{ background: '#111827', border: '1px solid #374151', borderRadius: 12, padding: 20 }}>
                        <h2 style={{ margin: '0 0 12px', fontSize: 20 }}>Recent scans</h2>
                        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                            <thead>
                                <tr style={{ color: '#94a3b8', fontSize: 12, textAlign: 'left' }}>
                                    <th style={{ padding: '8px 0' }}>File</th>
                                    <th style={{ padding: '8px 0' }}>Status</th>
                                    <th style={{ padding: '8px 0' }}>Time</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td style={{ padding: '10px 0' }}>invoice.pdf</td>
                                    <td style={{ color: '#22c55e' }}>Clean</td>
                                    <td>10:42</td>
                                </tr>
                                <tr>
                                    <td style={{ padding: '10px 0' }}>payload.exe</td>
                                    <td style={{ color: '#ef4444' }}>Threat</td>
                                    <td>09:11</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>

                    <aside style={{ background: '#111827', border: '1px solid #374151', borderRadius: 12, padding: 20 }}>
                        <h2 style={{ margin: '0 0 16px', fontSize: 20 }}>ClamAV Status</h2>
                        <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 8 }}>
                            <span style={{ width: 10, height: 10, borderRadius: '50%', background: '#22c55e', display: 'inline-block' }} />
                            Signature database up to date
                        </div>
                        <div>Last update: 2026-09-20 18:22 UTC</div>
                    </aside>
                </section>
            </div>
        </main>
    );
}
