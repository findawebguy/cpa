// CPA Exam Platform - Async REST API Client Module

// Automatically detect subpath for reverse proxies (e.g. /cpa or /)
const getApiBaseUrl = () => {
    const path = window.location.pathname || "";
    if (path.startsWith("/cpa")) {
        return "/cpa/api/v1";
    }
    return "/api/v1";
};

const API_BASE_URL = getApiBaseUrl();

class CPAApiClient {
    constructor() {
        this.token = localStorage.getItem("cpa_jwt_token") || null;
    }

    setToken(token) {
        this.token = token;
        if (token) {
            localStorage.setItem("cpa_jwt_token", token);
            document.cookie = `cpa_jwt_token=${token}; path=/; max-age=2592000; SameSite=Lax`;
        } else {
            localStorage.removeItem("cpa_jwt_token");
            document.cookie = `cpa_jwt_token=; path=/; max-age=0`;
        }
    }

    getHeaders() {
        const headers = {
            "Content-Type": "application/json"
        };
        if (this.token) {
            headers["Authorization"] = `Bearer ${this.token}`;
        }
        return headers;
    }

    async request(endpoint, options = {}) {
        const url = `${API_BASE_URL}${endpoint}`;
        const config = {
            ...options,
            headers: {
                ...this.getHeaders(),
                ...(options.headers || {})
            }
        };

        try {
            let response = await fetch(url, config);

            // Auto-recovery for expired/stale tokens: clear token and retry as guest
            if (response.status === 401 && this.token && !endpoint.includes("/auth/login")) {
                console.warn(`[API] 401 Unauthorized on ${endpoint}. Token expired/invalid. Clearing token & retrying...`);
                this.setToken(null);
                const retryConfig = {
                    ...options,
                    headers: {
                        ...this.getHeaders(),
                        ...(options.headers || {})
                    }
                };
                response = await fetch(url, retryConfig);
            }

            if (!response.ok) {
                const errData = await response.json().catch(() => ({ detail: "Network error" }));
                let msg = "HTTP Error " + response.status;
                if (errData.detail) {
                    if (Array.isArray(errData.detail)) {
                        msg = errData.detail.map(e => `${e.loc ? e.loc.join('.') : 'field'}: ${e.msg}`).join("; ");
                    } else if (typeof errData.detail === 'string') {
                        msg = errData.detail;
                    } else {
                        msg = JSON.stringify(errData.detail);
                    }
                }
                throw new Error(msg);
            }
            return await response.json();
        } catch (err) {
            console.error(`API Error on [${endpoint}]:`, err);
            throw err;
        }
    }

    // Auth API
    async login(email, password) {
        const res = await this.request("/auth/login", {
            method: "POST",
            body: JSON.stringify({ email, password })
        });
        if (res.access_token) {
            this.setToken(res.access_token);
        }
        return res;
    }

    async register(email, password) {
        const res = await this.request("/auth/register", {
            method: "POST",
            body: JSON.stringify({ email, password })
        });
        if (res.access_token) {
            this.setToken(res.access_token);
        }
        return res;
    }

    async getUserProfile() {
        return await this.request("/auth/user/profile");
    }

    async updateUserProfile(userData) {
        return await this.request("/auth/user/profile", {
            method: "PUT",
            body: JSON.stringify(userData)
        });
    }

    async migrateGuestSession(guestProgress = [], tbsCode = null, tbsRows = null) {
        return await this.request("/auth/migrate-guest-session", {
            method: "POST",
            body: JSON.stringify({
                guest_progress: guestProgress,
                tbs_code: tbsCode,
                tbs_rows: tbsRows
            })
        });
    }

    async generateQRSession() {
        return await this.request("/auth/qr-session", {
            method: "POST"
        });
    }

    async checkQRStatus(qrToken) {
        return await this.request(`/auth/qr-status?qr_token=${encodeURIComponent(qrToken)}`);
    }

    async qrLogin(qrToken) {
        const res = await this.request(`/auth/qr-login?qr_token=${encodeURIComponent(qrToken)}`);
        if (res.access_token) {
            this.setToken(res.access_token);
        }
        return res;
    }

    // Curriculum API
    async getCourses() {
        return await this.request("/courses");
    }

    async getSyllabus(trackCode) {
        return await this.request(`/courses/${trackCode}/syllabus`);
    }

    async getNode(nodeKey) {
        return await this.request(`/nodes/${nodeKey}`);
    }

    async submitNodeAnswer(nodeKey, selectedIndex, confidence) {
        return await this.request(`/nodes/${nodeKey}/submit`, {
            method: "POST",
            body: JSON.stringify({ index: selectedIndex, confidence })
        });
    }

    // Task-Based Simulation API
    async getTBS(simulationCode = "tbs-1") {
        return await this.request(`/tbs/${simulationCode}`);
    }

    async submitTBS(simulationCode = "tbs-1", rows = []) {
        return await this.request(`/tbs/${simulationCode}/submit`, {
            method: "POST",
            body: JSON.stringify({ rows })
        });
    }

    // Flashcards API
    async getFlashcards(domain = "FAR") {
        return await this.request(`/flashcards?domain=${domain}`);
    }

    async rateFlashcard(cardId, rating) {
        return await this.request(`/flashcards/${cardId}/rate`, {
            method: "POST",
            body: JSON.stringify({ rating })
        });
    }

    // Analytics API
    async getDiagnostics() {
        return await this.request("/analytics/diagnostics");
    }

    // Testing & QA Reset API
    async resetUserProgress() {
        return await this.request("/auth/user/reset", {
            method: "POST"
        });
    }

    // Record visiting an end node (marks week as completed)
    async visitNode(nodeKey) {
        return await this.request(`/nodes/${nodeKey}/visit`, {
            method: "POST"
        });
    }

    // Admin: Re-seed curriculum data
    async reseedCurriculum() {
        return await this.request("/auth/admin/reseed", {
            method: "POST"
        });
    }

    // Admin: Mark a specific week as completed
    async adminCompleteWeek(track, weekNumber) {
        return await this.request("/auth/admin/complete-week", {
            method: "POST",
            body: JSON.stringify({ track, week_number: weekNumber })
        });
    }

    // --- CASE STUDIES ---

    async getCaseStudies(courseId) {
        return await this.request(`/cases/course/${courseId}`);
    }

    async getCaseDetails(caseId) {
        return await this.request(`/cases/${caseId}`);
    }

    async submitCaseStudy(caseId, answers) {
        return await this.request(`/cases/${caseId}/submit`, {
            method: "POST",
            body: JSON.stringify({ answers })
        });
    }

    async triggerDailyLiveNewsIngestion(rawFeed = null) {
        return await this.request("/cases/live-news/trigger-daily-ingestion", {
            method: "POST",
            body: JSON.stringify(rawFeed ? { raw_feed: rawFeed } : {})
        });
    }

    // Admin: Get syllabus overview with completion status
    async adminGetOverview() {
        return await this.request("/auth/admin/syllabus-overview");
    }

    // Study & Prep Hub API
    async getStudyModules(track = null) {
        const query = track ? `?track=${track}` : "";
        return await this.request(`/study/modules${query}`);
    }

    async getStudyModule(moduleId) {
        return await this.request(`/study/modules/${moduleId}`);
    }
}

window.cpaApi = new CPAApiClient();

