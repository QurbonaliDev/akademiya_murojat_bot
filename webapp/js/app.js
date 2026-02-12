/**
 * app.js - Full Premium Logic for Telegram Mini App
 * - Tailwind Design System
 * - 9-step Rating Flow
 * - Admin Dashboard & CRUD
 * - Multi-language Support
 */

const API_BASE = window.location.origin;
const tg = window.Telegram?.WebApp;

// Initial State
const state = {
    lang: 'uz',
    translations: {},
    config: {}, // Faculties, directions, types, etc.
    currentView: 'homeView',
    complaintData: {},
    ratingData: {
        step: 1,
        maxSteps: 9,
        answers: {}
    },
    adminStats: {}
};

/**
 * INITIALIZATION
 */
async function initApp() {
    if (tg) {
        tg.ready();
        tg.expand();
        // Set theme from Telegram
        if (tg.colorScheme === 'dark') document.documentElement.classList.add('dark');
        else document.documentElement.classList.remove('dark');
    }

    showLoading();
    try {
        await fetchConfig();
        applyTranslations();
        initNavigation();
        showView('homeView');
    } catch (err) {
        console.error('Initialization failed', err);
    } finally {
        hideLoading();
    }
}

/**
 * CONFIG & DATA FETCHING
 */
async function fetchConfig() {
    const user_id = tg?.initDataUnsafe?.user?.id || '';
    const response = await fetch(`${API_BASE}/api/config?lang=${state.lang}&user_id=${user_id}`);
    state.config = await response.json();
    state.translations = state.config.translations || {};

    // Check Admin Status
    if (state.config.is_admin) {
        document.getElementById('adminTabBtn')?.classList.remove('hidden');
    }
}

/**
 * TRANSLATIONS & L10N
 */
function t(key) {
    return state.translations[key] || key;
}

function applyTranslations() {
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        el.textContent = t(key);
    });

    // Update labels and placeholders
    document.getElementById('currentLang').textContent = state.lang.toUpperCase();
    document.getElementById('headerTitle').textContent = t('header_title') || 'Akademiya';
}

async function changeLanguage(newLang) {
    state.lang = newLang;
    showLoading();
    await fetchConfig();
    applyTranslations();
    toggleLangMenu(); // Close menu
    hideLoading();
}

function renderLanguages() {
    const menu = document.getElementById('langMenu');
    const langs = { uz: 'O\'zbekcha', ru: 'Русский', en: 'English' };
    menu.innerHTML = Object.entries(langs).map(([code, name]) => `
        <button onclick="changeLanguage('${code}')" class="w-full text-left px-3 py-2 text-xs font-semibold rounded-xl hover:bg-slate-100 dark:hover:bg-slate-700 transition-colors">
            ${name}
        </button>
    `).join('');
}

function toggleLangMenu() {
    const menu = document.getElementById('langMenu');
    menu.classList.toggle('hidden');
    if (!menu.classList.contains('hidden')) renderLanguages();
}

/**
 * VIEW MANAGEMENT
 */
function showView(viewId) {
    // Hide all
    document.querySelectorAll('.view').forEach(v => {
        v.classList.remove('active');
        v.classList.add('hidden');
    });

    // Show target
    const target = document.getElementById(viewId);
    if (target) {
        target.classList.remove('hidden');
        setTimeout(() => target.classList.add('active'), 50);
    }

    state.currentView = viewId;

    // Update Navigation Active State
    document.querySelectorAll('.nav-item').forEach(nav => nav.classList.remove('active'));
    const navMap = { homeView: 'navHome', complaintView: 'navComplaint', ratingView: 'navRating', rulesView: 'navRules' };
    if (navMap[viewId]) document.getElementById(navMap[viewId])?.classList.add('active');

    // View specific initializers
    if (viewId === 'complaintView') initComplaintFlow();
    if (viewId === 'ratingView') initRatingFlow();
    if (viewId === 'rulesView') renderRules();
    if (viewId === 'surveyView') renderSurveys();
    if (viewId === 'adminDashboardView') loadAdminDashboard();

    // Scroll to top
    window.scrollTo(0, 0);

    // Lucide
    if (window.lucide) window.lucide.createIcons();
}

/**
 * COMPLAINT FLOW
 */
function initComplaintFlow() {
    state.complaintData = { step: 1, answers: {} };
    renderComplaintStep(1);
}

function renderComplaintStep(step) {
    state.complaintData.step = step;
    const container = document.getElementById('complaintStepContainer');
    container.innerHTML = '';

    switch (step) {
        case 1: // Faculty
            container.innerHTML = `<h3 class="text-lg font-bold mb-4">${t('choose_faculty')}</h3><div class="space-y-3" id="complaintStepContent"></div>`;
            state.config.faculties?.forEach(f => appendComplaintOption(t(f.translation_key), 'university', () => {
                state.complaintData.answers.faculty = f.code;
                renderComplaintStep(2);
            }));
            break;
        case 2: // Direction
            container.innerHTML = `<h3 class="text-lg font-bold mb-4">${t('choose_direction')}</h3><div class="space-y-3" id="complaintStepContent"></div>`;
            const directions = state.config.directions?.filter(d => d.faculty_code === state.complaintData.answers.faculty) || [];
            directions.forEach(d => appendComplaintOption(t(d.translation_key), 'graduation-cap', () => {
                state.complaintData.answers.direction = d.code;
                if (state.complaintData.answers.faculty === 'magistratura') renderComplaintStep(5);
                else renderComplaintStep(3);
            }));
            break;
        case 3: // Edu Type
            container.innerHTML = `<h3 class="text-lg font-bold mb-4">${t('choose_edu_type')}</h3><div class="space-y-3" id="complaintStepContent"></div>`;
            state.config.education_types?.forEach(et => appendComplaintOption(t(et.translation_key), 'book-open', () => {
                state.complaintData.answers.edu_type = et.code;
                renderComplaintStep(4);
            }));
            break;
        case 4: // Edu Lang
            container.innerHTML = `<h3 class="text-lg font-bold mb-4">${t('choose_edu_lang')}</h3><div class="space-y-3" id="complaintStepContent"></div>`;
            state.config.education_languages?.forEach(el => appendComplaintOption(t(el.translation_key), 'languages', () => {
                state.complaintData.answers.edu_lang = el.code;
                renderComplaintStep(5);
            }));
            break;
        case 5: // Course
            container.innerHTML = `<h3 class="text-lg font-bold mb-4">${t('choose_course')}</h3><div class="space-y-3" id="complaintStepContent"></div>`;
            const type = state.complaintData.answers.faculty === 'magistratura' ? 'magistr' : 'regular';
            state.config.courses?.[type]?.forEach(c => appendComplaintOption(t(c.translation_key), 'hash', () => {
                state.complaintData.answers.course = c.code;
                renderComplaintStep(6);
            }));
            break;
        case 6: // Complaint Type
            container.innerHTML = `<h3 class="text-lg font-bold mb-4">${t('choose_complaint_type')}</h3><div class="space-y-3" id="complaintStepContent"></div>`;
            state.config.complaint_types?.forEach(ct => appendComplaintOption(t(ct.translation_key), 'info', () => {
                state.complaintData.answers.type = ct.code;
                state.complaintData.currentTypeInfo = ct;
                if (ct.requires_subject) renderComplaintStep(7);
                else if (ct.requires_teacher) renderComplaintStep(8);
                else renderComplaintStep(9);
            }));
            break;
        case 7: // Subject
            container.innerHTML = `
                <h3 class="text-lg font-bold mb-4">${t('enter_subject')}</h3>
                <input type="text" id="compSubject" class="input-field mb-6" placeholder="${t('subject_placeholder')}">
                <button onclick="saveComplaintInput('subject', 'compSubject')" class="btn-primary w-full">${t('btn_next')}</button>
            `;
            break;
        case 8: // Teacher
            container.innerHTML = `
                <h3 class="text-lg font-bold mb-4">${t('enter_teacher')}</h3>
                <input type="text" id="compTeacher" class="input-field mb-6" placeholder="${t('teacher_placeholder')}">
                <button onclick="saveComplaintInput('teacher', 'compTeacher')" class="btn-primary w-full">${t('btn_next')}</button>
            `;
            break;
        case 9: // Message
            container.innerHTML = `
                <h3 class="text-lg font-bold mb-4">${t('enter_message')}</h3>
                <textarea id="compMessage" class="input-field h-40 mb-6" placeholder="${t('message_placeholder')}"></textarea>
                <button onclick="submitComplaint()" class="btn-primary w-full">
                    <i data-lucide="send" class="w-5 h-5"></i>
                    ${t('btn_send')}
                </button>
            `;
            break;
    }
    if (window.lucide) window.lucide.createIcons();
}

function appendComplaintOption(label, icon, onClick) {
    const el = createOptionCard(label, icon, onClick);
    document.getElementById('complaintStepContent').appendChild(el);
}

function saveComplaintInput(key, inputId) {
    const val = document.getElementById(inputId).value;
    if (!val) return tg?.showAlert(t('error_fill_field'));
    state.complaintData.answers[key] = val;

    const info = state.complaintData.currentTypeInfo;
    if (key === 'subject' && info.requires_teacher) renderComplaintStep(8);
    else renderComplaintStep(9);
}

async function submitComplaint() {
    const message = document.getElementById('compMessage').value;
    state.complaintData.answers.message = message;

    // Map internal keys to backend keys
    const payload = {
        user_id: tg?.initDataUnsafe?.user?.id || 'web_user',
        faculty: state.complaintData.answers.faculty,
        direction: state.complaintData.answers.direction,
        course: state.complaintData.answers.course,
        education_type: state.complaintData.answers.edu_type,
        education_language: state.complaintData.answers.edu_lang,
        complaint_type: state.complaintData.answers.type,
        subject_name: state.complaintData.answers.subject,
        teacher_name: state.complaintData.answers.teacher,
        message: state.complaintData.answers.message
    };

    showLoading();
    try {
        const response = await fetch(`${API_BASE}/api/complaint`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (response.ok) showView('successView');
        else throw new Error('Submission failed');
    } catch (err) {
        tg?.showAlert(t('error_unknown'));
    } finally {
        hideLoading();
    }
}

window.saveComplaintInput = saveComplaintInput;
window.submitComplaint = submitComplaint;

/**
 * RATING FLOW (9 STEPS)
 */
function initRatingFlow() {
    state.ratingData = { step: 1, maxSteps: 9, answers: {} };
    renderRatingStep(1);
}

function updateRatingProgress() {
    const progress = (state.ratingData.step / state.ratingData.maxSteps) * 100;
    document.getElementById('ratingProgressBar').style.width = `${progress}%`;
}

function renderRatingStep(step) {
    state.ratingData.step = step;
    updateRatingProgress();
    const container = document.getElementById('ratingStepContainer');
    container.innerHTML = '';

    switch (step) {
        case 1: // Faculty
            container.innerHTML = `<h3 class="text-lg font-bold mb-4">${t('choose_faculty')}</h3><div class="space-y-3" id="stepContent"></div>`;
            state.config.faculties?.forEach(item => {
                appendOption(t(item.translation_key), () => {
                    state.ratingData.answers.faculty = item.code;
                    renderRatingStep(2);
                }, 'university');
            });
            break;
        case 2: // Direction
            container.innerHTML = `<h3 class="text-lg font-bold mb-4">${t('choose_direction')}</h3><div class="space-y-3" id="stepContent"></div>`;
            const directions = state.config.directions?.filter(d => d.faculty_code === state.ratingData.answers.faculty) || [];
            directions.forEach(item => {
                appendOption(t(item.translation_key), () => {
                    state.ratingData.answers.direction = item.code;
                    // Skip edu_type for magistratura
                    if (state.ratingData.answers.faculty === 'magistratura') renderRatingStep(5);
                    else renderRatingStep(3);
                }, 'graduation-cap');
            });
            break;
        case 3: // Edu Type
            container.innerHTML = `<h3 class="text-lg font-bold mb-4">${t('choose_edu_type')}</h3><div class="space-y-3" id="stepContent"></div>`;
            state.config.education_types?.forEach(item => {
                appendOption(t(item.translation_key), () => {
                    state.ratingData.answers.edu_type = item.code;
                    renderRatingStep(4);
                }, 'book-open');
            });
            break;
        case 4: // Edu Lang
            container.innerHTML = `<h3 class="text-lg font-bold mb-4">${t('choose_edu_lang')}</h3><div class="space-y-3" id="stepContent"></div>`;
            state.config.education_languages?.forEach(item => {
                appendOption(t(item.translation_key), () => {
                    state.ratingData.answers.edu_lang = item.code;
                    renderRatingStep(5);
                }, 'languages');
            });
            break;
        case 5: // Course
            container.innerHTML = `<h3 class="text-lg font-bold mb-4">${t('choose_course')}</h3><div class="space-y-3" id="stepContent"></div>`;
            const courseType = state.ratingData.answers.faculty === 'magistratura' ? 'magistr' : 'regular';
            state.config.courses?.[courseType]?.forEach(item => {
                appendOption(t(item.translation_key), () => {
                    state.ratingData.answers.course = item.code;
                    renderRatingStep(6);
                }, 'hash');
            });
            break;
        case 6: // Subject Name
            container.innerHTML = `
                <h3 class="text-lg font-bold mb-4">${t('enter_subject')}</h3>
                <input type="text" id="subjectInput" class="input-field mb-6" placeholder="${t('subject_placeholder') || 'Fan nomi...'}">
                <button onclick="saveRatingInput('subject_name', 'subjectInput', 7)" class="btn-primary w-full">${t('btn_next')}</button>
            `;
            break;
        case 7: // Teacher Name
            container.innerHTML = `
                <h3 class="text-lg font-bold mb-4">${t('enter_teacher')}</h3>
                <input type="text" id="teacherInput" class="input-field mb-6" placeholder="${t('teacher_placeholder') || 'O\'qituvchi ismi...'}">
                <button onclick="saveRatingInput('teacher_name', 'teacherInput', 8)" class="btn-primary w-full">${t('btn_next')}</button>
            `;
            break;
        case 8: // Rating Questions
            container.innerHTML = `<h3 class="text-lg font-bold mb-4">${t('btn_lesson_rating')}</h3><div class="space-y-6" id="questionsList"></div>`;
            renderRatingQuestions();
            break;
        case 9: // Final Comment
            container.innerHTML = `
                <h3 class="text-lg font-bold mb-4">${t('enter_comment')}</h3>
                <textarea id="ratingComment" class="input-field h-40 mb-6" placeholder="${t('comment_placeholder') || 'Batafsil fikringiz...'}"></textarea>
                <button onclick="submitRating()" class="btn-primary w-full bg-green-500 hover:bg-green-600">
                    <i data-lucide="send" class="w-5 h-5"></i>
                    ${t('btn_send')}
                </button>
            `;
            break;
    }

    if (window.lucide) window.lucide.createIcons();
}

function saveRatingInput(key, inputId, nextStep) {
    const val = document.getElementById(inputId).value;
    if (!val) return tg?.showAlert(t('error_fill_field'));
    state.ratingData.answers[key] = val;
    renderRatingStep(nextStep);
}

function renderRatingQuestions() {
    const container = document.getElementById('questionsList');
    state.config.rating_questions?.forEach(q => {
        const qEl = document.createElement('div');
        qEl.className = 'space-y-3';
        qEl.innerHTML = `<p class="font-semibold text-sm">${t(q.translation_key)}</p>`;

        const opts = document.createElement('div');
        opts.className = 'grid grid-cols-5 gap-2';

        if (q.answer_type === 'scale') {
            for (let i = 1; i <= 5; i++) {
                const btn = document.createElement('button');
                btn.className = 'h-12 rounded-xl bg-slate-100 dark:bg-slate-800 font-bold active:bg-primary active:text-white transition-all';
                btn.textContent = i;
                btn.onclick = () => {
                    state.ratingData.answers[`q${q.question_number}`] = i;
                    btn.parentElement.querySelectorAll('button').forEach(b => b.classList.replace('bg-primary', 'bg-slate-100'));
                    btn.classList.add('bg-primary', 'text-white');
                    checkRatingCompletion();
                };
                opts.appendChild(btn);
            }
        } else {
            // Yes/No logic...
        }
        qEl.appendChild(opts);
        container.appendChild(qEl);
    });

    const nextBtn = document.createElement('button');
    nextBtn.className = 'btn-primary w-full mt-8';
    nextBtn.textContent = t('btn_next');
    nextBtn.onclick = () => renderRatingStep(9);
    container.appendChild(nextBtn);
}

function checkRatingCompletion() {
    // Check if all questions answered if needed
}

async function submitRating() {
    const comment = document.getElementById('ratingComment').value;
    state.ratingData.answers.comment = comment;

    showLoading();
    try {
        const response = await fetch(`${API_BASE}/api/rating`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                user_id: tg?.initDataUnsafe?.user?.id || 'web_user',
                ...state.ratingData.answers
            })
        });

        if (response.ok) showView('successView');
        else throw new Error('Rating submission failed');
    } catch (err) {
        tg?.showAlert(t('error_unknown'));
    } finally {
        hideLoading();
    }
}

/**
 * ADMIN FUNCTIONS
 */
async function loadAdminDashboard() {
    showLoading();
    try {
        const resp = await fetch(`${API_BASE}/api/admin/dashboard`);
        const stats = await resp.json();
        document.getElementById('statsToday').textContent = stats.today || 0;
        document.getElementById('statsWeek').textContent = stats.week || 0;
        document.getElementById('statsMonth').textContent = stats.month || 0;
    } catch (err) {
        console.error('Admin dashboard failed', err);
    } finally {
        hideLoading();
    }
}

async function showAdminSettings(type) {
    state.currentSettingType = type;
    showView('adminSettingsView');
    document.getElementById('settingsTitle').textContent = t(`btn_manage_${type}`);
    loadSettingsList(type);
}

async function loadSettingsList(type) {
    const container = document.getElementById('settingsList');
    container.innerHTML = '<div class="py-10 text-center text-slate-400">Loading settings...</div>';

    try {
        const resp = await fetch(`${API_BASE}/api/admin/settings/${type}`);
        const data = await resp.json();
        container.innerHTML = '';

        data.items?.forEach(item => {
            const card = document.createElement('div');
            card.className = 'card flex items-center justify-between p-4';

            // Format display label
            let label = item[1] || item[0];
            if (type === 'questions') label = t(item[1]);

            card.innerHTML = `
                <div>
                    <p class="font-bold text-sm text-slate-800 dark:text-slate-200">${label}</p>
                    <p class="text-[10px] text-slate-400 dark:text-slate-500 font-mono italic">${item[0]}</p>
                </div>
                <div class="flex gap-2">
                    <button class="w-8 h-8 rounded-lg bg-blue-50 dark:bg-blue-900/30 text-blue-500 flex items-center justify-center active:scale-90 transition-all">
                        <i data-lucide="edit-3" class="w-4 h-4"></i>
                    </button>
                    <button onclick="deleteSettingItem('${type}', '${item[0]}')" class="w-8 h-8 rounded-lg bg-red-50 dark:bg-red-900/30 text-red-500 flex items-center justify-center active:scale-90 transition-all">
                        <i data-lucide="trash-2" class="w-4 h-4"></i>
                    </button>
                </div>
            `;
            container.appendChild(card);
        });

        if (!data.items?.length) {
            container.innerHTML = '<div class="py-10 text-center text-slate-400 italic">Ma\'lumot topilmadi</div>';
        }

        if (window.lucide) window.lucide.createIcons();
    } catch (err) {
        container.innerHTML = '<div class="py-10 text-center text-red-400">Error loading settings</div>';
    }
}

function openAddModal() {
    const type = state.currentSettingType;
    const content = document.getElementById('modalContent');
    content.innerHTML = `
        <div class="flex items-center justify-between mb-6">
            <h2 class="text-xl font-bold">${t('btn_add_new')}</h2>
            <button onclick="closeModal()" class="w-10 h-10 rounded-full bg-slate-100 dark:bg-slate-800 flex items-center justify-center">
                <i data-lucide="x" class="w-5 h-5"></i>
            </button>
        </div>
        <div class="space-y-4">
            <input type="text" id="addInput1" class="input-field" placeholder="ID / Code">
            <input type="text" id="addInput2" class="input-field" placeholder="Name / Title">
            <button onclick="saveNewSetting()" class="btn-primary w-full mt-4">Save</button>
        </div>
    `;
    openModal();
}

async function saveNewSetting() {
    // Basic Add logic (Simplified)
    tg?.showAlert('Bu qism tez orada bot yordamida yakunlanadi (Backend check)');
    closeModal();
}

async function deleteSettingItem(type, id) {
    if (!confirm(t('confirm_delete') || 'O\'chirshni tasdiqlaysizmi?')) return;
    showLoading();
    try {
        const resp = await fetch(`${API_BASE}/api/admin/settings/${type}/${id}`, { method: 'DELETE' });
        if (resp.ok) loadSettingsList(type);
        else throw new Error('Delete failed');
    } catch (err) {
        tg?.showAlert(t('error_unknown'));
    } finally {
        hideLoading();
    }
}

window.openAddModal = openAddModal;
window.saveNewSetting = saveNewSetting;
window.deleteSettingItem = deleteSettingItem;

/**
 * HELPERS
 */
function createOptionCard(label, iconName, onClick) {
    const div = document.createElement('div');
    div.className = 'card flex items-center gap-4 hover:border-primary cursor-pointer active:scale-95 transition-all';
    div.onclick = onClick;
    div.innerHTML = `
        <div class="w-10 h-10 rounded-xl bg-slate-100 dark:bg-slate-800 flex items-center justify-center text-slate-500">
            <i data-lucide="${iconName}" class="w-5 h-5"></i>
        </div>
        <span class="font-semibold">${label}</span>
    `;
    return div;
}

/**
 * RULES & SURVEYS
 */
function renderRules() {
    const container = document.getElementById('rulesList');
    container.innerHTML = '';
    const rules = [
        { id: 'general', title: 'btn_rules_general', icon: 'info' },
        { id: 'grading', title: 'btn_rules_grading', icon: 'award' },
        { id: 'exam', title: 'btn_rules_exam', icon: 'file-text' }
    ];

    rules.forEach(rule => {
        const card = createOptionCard(t(rule.title), rule.icon, () => openRuleDetail(rule.id));
        container.appendChild(card);
    });
}

function openRuleDetail(ruleId) {
    const content = document.getElementById('modalContent');
    const text = t(`rules_${ruleId}_content`) || 'Tez orada...';
    content.innerHTML = `
        <div class="flex items-center justify-between mb-6">
            <h2 class="text-xl font-bold">${t(`btn_rules_${ruleId}`)}</h2>
            <button onclick="closeModal()" class="w-10 h-10 rounded-full bg-slate-100 dark:bg-slate-800 flex items-center justify-center">
                <i data-lucide="x" class="w-5 h-5"></i>
            </button>
        </div>
        <div class="prose dark:prose-invert max-w-none text-slate-600 dark:text-slate-400">
            ${text.replace(/\n/g, '<br>')}
        </div>
    `;
    openModal();
}

function renderSurveys() {
    const container = document.getElementById('surveyList');
    container.innerHTML = '';
    state.config.surveys?.forEach(s => {
        const card = createOptionCard(t(s.translation_key), 'external-link', () => tg?.openLink(s.url));
        container.appendChild(card);
    });
}

/**
 * MODALS
 */
function openModal() {
    const modal = document.getElementById('customModal');
    const content = document.getElementById('modalContent');
    modal.classList.remove('hidden');
    setTimeout(() => content.classList.replace('translate-y-full', 'translate-y-0'), 10);
    if (window.lucide) window.lucide.createIcons();
}

function closeModal() {
    const modal = document.getElementById('customModal');
    const content = document.getElementById('modalContent');
    content.classList.replace('translate-y-0', 'translate-y-full');
    setTimeout(() => modal.classList.add('hidden'), 300);
}

window.closeModal = closeModal;

/**
 * RESET & UTILS
 */
function resetForm() {
    initApp();
}

window.resetForm = resetForm;

function showLoading() { document.getElementById('loadingOverlay').classList.remove('hidden'); }
function hideLoading() { document.getElementById('loadingOverlay').classList.add('hidden'); }

function initNavigation() {
    // Close lang menu on body click
    document.addEventListener('click', (e) => {
        if (!e.target.closest('.lang-switcher')) document.getElementById('langMenu').classList.add('hidden');
    });
}

// Global Exports
window.showView = showView;
window.toggleLangMenu = toggleLangMenu;
window.changeLanguage = changeLanguage;
window.saveRatingInput = saveRatingInput;
window.submitRating = submitRating;
window.showAdminSettings = showAdminSettings;

// Start the app
initApp();
