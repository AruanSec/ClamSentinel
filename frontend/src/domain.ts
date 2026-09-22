export type ScanStatus = 'CLEAN' | 'INFECTED' | 'ERROR' | 'SCANNING';

export interface ScanSummary {
    id: string;
    filename: string;
    status: ScanStatus;
    time: string;
}

export interface DashboardStat {
    label: string;
    value: string;
}

export interface DashboardData {
    status: 'Healthy' | 'Degraded';
    stats: DashboardStat[];
    recentScans: ScanSummary[];
    lastUpdated: string;
}