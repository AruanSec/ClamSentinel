import { NavLink, Navigate, Route, Routes } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { getDashboard } from './services/mockApi';

const navigation = [
    { label: 'Dashboard', path: '/' },
    { label: 'Quick Scan', path: '/scan' },
    { label: 'Scan History', path: '/history' },
    { label: 'Quarantine', path: '/quarantine' },
    { label: 'Virus Definitions', path: '/definitions' },
    { label: 'Observability', path: '/observability' },
    { label: 'Settings', path: '/settings' },
];

function Dashboard() {
    const { data } = useQuery({ queryKey: ['dashboard'], queryFn: getDashboard });

    if (!data) {
        return <p>Loading dashboard...</p>;
    }

    return (
        <>
            <header className="page-header">
                <div>
                    <div className="eyebrow">ClamSentinel</div>
                    <h1>Operations Dashboard</h1>
                </div>
                <div className="status-pill">Status: {data.status}</div>
            </header>

            <section className="stats-grid">
                {data.stats.map((stat) => (
                    <div className="panel stat-card" key={stat.label}>
                        <div className="muted">{stat.label}</div>
                        <div className="stat-value">{stat.value}</div>
                    </div>
                ))}
            </section>

            <section className="dashboard-grid">
                <div className="panel">
                    <h2>Recent scans</h2>
                    <table>
                        <thead>
                            <tr>
                                <th>File</th>
                                <th>Status</th>
                                <th>Time</th>
                            </tr>
                        </thead>
                        <tbody>
                            {data.recentScans.map((scan) => (
                                <tr key={scan.id}>
                                    <td>{scan.filename}</td>
                                    <td className={`scan-status ${scan.status.toLowerCase()}`}>{scan.status}</td>
                                    <td>{scan.time}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>

                <aside className="panel">
                    <h2>ClamAV Status</h2>
                    <p className="status-line"><span className="status-dot" />Signature database up to date</p>
                    <p className="muted">Last update: {data.lastUpdated}</p>
                </aside>
            </section>
        </>
    );
}

function PlaceholderPage({ title }: { title: string }) {
    return (
        <section className="panel placeholder-page">
            <div className="eyebrow">Phase 2 foundation</div>
            <h1>{title}</h1>
            <p className="muted">This route is connected and ready for its feature implementation.</p>
        </section>
    );
}

function AppShell() {
    return (
        <div className="app-shell">
            <aside className="sidebar">
                <div className="brand">ClamSentinel</div>
                <nav aria-label="Primary navigation">
                    {navigation.map((item) => (
                        <NavLink className={({ isActive }) => isActive ? 'nav-link active' : 'nav-link'} end={item.path === '/'} key={item.path} to={item.path}>
                            {item.label}
                        </NavLink>
                    ))}
                </nav>
            </aside>
            <main className="content">
                <Routes>
                    <Route element={<Dashboard />} path="/" />
                    {navigation.slice(1).map((item) => <Route element={<PlaceholderPage title={item.label} />} key={item.path} path={item.path} />)}
                    <Route element={<Navigate replace to="/" />} path="*" />
                </Routes>
            </main>
        </div>
    );
}

export default function App() {
    return (
        <AppShell />
    );
}
