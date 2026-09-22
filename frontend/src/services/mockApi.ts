import type { DashboardData } from '../domain';

export async function getDashboard(): Promise<DashboardData> {
    return {
        status: 'Healthy',
        stats: [
            { label: 'Protected files', value: '842' },
            { label: 'Threats found', value: '17' },
            { label: 'Avg scan', value: '112 ms' },
            { label: 'System health', value: 'Healthy' },
        ],
        recentScans: [
            { id: 'scan-001', filename: 'invoice.pdf', status: 'CLEAN', time: '10:42' },
            { id: 'scan-002', filename: 'payload.exe', status: 'INFECTED', time: '09:11' },
        ],
        lastUpdated: '2026-09-20 18:22 UTC',
    };
}