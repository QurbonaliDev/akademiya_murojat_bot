// app.js - Mini App JavaScript

// ============================================
// GLOBAL STATE
// ============================================
const state = {
    currentStep: 1,
    totalSteps: 8,
    currentView: 'homeView',
    language: 'uz',
    translations: {},
    config: null,
    formData: {},
    ratingData: {
        step: 1,
        faculty: null,
        direction: null,
        course: null,
        edu_type: null,
        edu_lang: null,
        ratings: {},
        comment: ''
    }
};

// API Base URL (relative to current host)
const API_BASE = window.location.origin;

// ============================================
// TELEGRAM WEBAPP INTEGRATION
// ============================================
const tg = window.Telegram?.WebApp;

function initTelegram() {
    if (tg) {
        // Expand to full height
        tg.expand();

        // Apply theme colors
        document.body.classList.add('tg-theme');
        document.documentElement.style.setProperty('--tg-theme-bg-color', tg.themeParams.bg_color || '#ffffff');
        document.documentElement.style.setProperty('--tg-theme-text-color', tg.themeParams.text_color || '#000000');
        document.documentElement.style.setProperty('--tg-theme-hint-color', tg.themeParams.hint_color || '#999999');
        document.documentElement.style.setProperty('--tg-theme-link-color', tg.themeParams.link_color || '#2481cc');
        document.documentElement.style.setProperty('--tg-theme-button-color', tg.themeParams.button_color || '#2481cc');
        document.documentElement.style.setProperty('--tg-theme-button-text-color', tg.themeParams.button_text_color || '#ffffff');
        document.documentElement.style.setProperty('--tg-theme-secondary-bg-color', tg.themeParams.secondary_bg_color || '#f0f0f0');

        // Ready
        tg.ready();
        console.log('Telegram WebApp initialized');
    }
}

// ============================================
// API FUNCTIONS
// ============================================
async function fetchConfig() {
    showLoading();
    try {
        const response = await fetch(`${API_BASE}/api/config?lang=${state.language}`);
        if (!response.ok) throw new Error('Failed to fetch config');

        state.config = await response.json();
        state.translations = state.config.translations;

        applyTranslations();
        updateCurrentLangUI();
        renderLanguages();

        // Show Admin button if user is admin
        if (state.config.is_admin) {
            document.getElementById('adminTabBtn').style.display = 'flex';
        }

        console.log('Config loaded:', state.config);
    } catch (error) {
        console.error('Error fetching config:', error);
        showError('Ma\'lumotlarni yuklashda xatolik');
    } finally {
        hideLoading();
    }
}

async function fetchLanguages() {
    try {
        const response = await fetch(`${API_BASE}/api/languages`);
        return await response.json();
    } catch (error) {
        return { languages: [{ code: 'uz', name: 'O\'zbekcha' }] };
    }
}

async function changeLanguage(langCode) {
    state.language = langCode;
    toggleLangMenu(false);
    await fetchConfig();
    updateHeader(state.currentView);
}

function updateCurrentLangUI() {
    const el = document.getElementById('currentLang');
    if (el) el.textContent = state.language.toUpperCase();
}

async function renderLanguages() {
    const container = document.getElementById('langMenu');
    if (!container) return;

    const data = await fetchLanguages();
    container.innerHTML = '';

    data.languages?.forEach(lang => {
        const btn = document.createElement('button');
        btn.className = 'lang-item';
        btn.textContent = lang.name;
        btn.onclick = () => changeLanguage(lang.code);
        container.appendChild(btn);
    });
}

function toggleLangMenu(force) {
    const menu = document.getElementById('langMenu');
    if (force !== undefined) {
        menu.classList.toggle('active', force);
    } else {
        menu.classList.toggle('active');
    }
}

async function fetchDirections(facultyCode) {
    try {
        const response = await fetch(`${API_BASE}/api/directions/${facultyCode}`);
        if (!response.ok) throw new Error('Failed to fetch directions');
        return await response.json();
    } catch (error) {
        console.error('Error fetching directions:', error);
        return { directions: [] };
    }
}

async function submitComplaint(data) {
    showLoading();
    try {
        const response = await fetch(`${API_BASE}/api/complaint`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        const result = await response.json();
        if (result.success) {
            showView('successView');
        } else {
            showError(result.error || 'Xatolik yuz berdi');
        }
    } catch (error) {
        showError('Yuborishda xatolik');
    } finally { hideLoading(); }
}

async function submitRating() {
    showLoading();
    try {
        const payload = {
            faculty: state.ratingData.faculty,
            direction: state.ratingData.direction,
            course: state.ratingData.course,
            education_type: state.ratingData.edu_type,
            education_language: state.ratingData.edu_lang,
            ratings: state.ratingData.ratings,
            comment: document.getElementById('ratingComment').value
        };
        const response = await fetch(`${API_BASE}/api/rating`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        const result = await response.json();
        if (result.success) {
            showView('successView');
        } else {
            showError(result.error || 'Xatolik yuz berdi');
        }
    } catch (error) {
        showError('Yuborishda xatolik');
    } finally { hideLoading(); }
}

// ============================================
// VIEW NAVIGATION
// ============================================
function showView(viewId) {
    document.querySelectorAll('.view').forEach(view => view.classList.remove('active'));
    const view = document.getElementById(viewId);
    if (view) {
        view.classList.add('active');
        state.currentView = viewId;
    }
    updateHeader(viewId);

    // Initializers
    if (viewId === 'complaintView') initComplaintForm();
    if (viewId === 'ratingView') initRatingForm();
    if (viewId === 'rulesView') renderRulesList();
    if (viewId === 'surveyView') renderSurveyList();
    if (viewId === 'adminDashboardView') loadAdminDashboard();

    // Telegram Back Button
    if (tg) {
        if (viewId === 'homeView') {
            tg.BackButton.hide();
        } else {
            tg.BackButton.show();
            tg.BackButton.onClick(() => {
                if (state.currentView === 'complaintView') prevStep();
                else if (state.currentView === 'ratingView') prevRatingStep();
                else showView('homeView');
            });
        }
    }
}

function updateHeader(viewId) {
    const subtitle = document.getElementById('headerSubtitle');
    const titles = {
        homeView: t('welcome') || 'Xush kelibsiz!',
        complaintView: t('choose_faculty') || 'Murojaat yuborish',
        rulesView: t('btn_rules') || 'Tartib qoidalar',
        surveyView: t('btn_survey') || 'So\'rovnomalar',
        ratingView: t('btn_lesson_rating') || 'Dars baholash',
        successView: t('complaint_accepted') || 'Muvaffaqiyatli!'
    };
    subtitle.textContent = titles[viewId] || '';
}

// ============================================
// COMPLAINT FORM
// ============================================
function initComplaintForm() {
    state.currentStep = 1;
    state.formData = {
        faculty: null,
        direction: null,
        education_type: null,
        education_language: null,
        course: null,
        complaint_type: null,
        subject_name: '',
        teacher_name: '',
        message: ''
    };

    // Render faculty buttons
    renderFacultyButtons();

    // Show first step
    showStep(1);
    updateFormNav();
}

function showStep(stepNum) {
    document.querySelectorAll('.form-step').forEach(step => {
        step.classList.remove('active');
    });

    const step = document.getElementById(`step${stepNum}`);
    if (step) {
        step.classList.add('active');
        state.currentStep = stepNum;
    }

    updateFormNav();
}

function nextStep() {
    const faculty = state.formData.faculty;

    // Skip education type/lang for magistratura
    if (faculty === 'magistratura') {
        if (state.currentStep === 2) {
            showStep(5); // Skip to course
            renderCourseButtons();
            return;
        }
    }

    // Validate current step
    if (!validateCurrentStep()) return;

    // Move to next step
    const nextStepNum = state.currentStep + 1;

    // Skip step 7 if complaint type doesn't require subject/teacher
    if (nextStepNum === 7) {
        const complaintType = state.config.complaint_types.find(
            ct => ct.code === state.formData.complaint_type
        );
        if (!complaintType?.requires_subject && !complaintType?.requires_teacher) {
            showStep(8);
            return;
        }
    }

    if (nextStepNum <= state.totalSteps) {
        showStep(nextStepNum);
        prepareStep(nextStepNum);
    }
}

function prevStep() {
    const faculty = state.formData.faculty;
    const prevStepNum = state.currentStep - 1;

    // Handle back from magistratura course selection
    if (faculty === 'magistratura' && state.currentStep === 5) {
        showStep(2);
        return;
    }

    // Handle back from message step if subject/teacher not required
    if (state.currentStep === 8) {
        const complaintType = state.config?.complaint_types?.find(
            ct => ct.code === state.formData.complaint_type
        );
        if (!complaintType?.requires_subject && !complaintType?.requires_teacher) {
            showStep(6);
            return;
        }
    }

    if (prevStepNum >= 1) {
        showStep(prevStepNum);
    } else {
        showView('homeView');
    }
}

function validateCurrentStep() {
    switch (state.currentStep) {
        case 1:
            return !!state.formData.faculty;
        case 2:
            return !!state.formData.direction;
        case 3:
            return !!state.formData.education_type;
        case 4:
            return !!state.formData.education_language;
        case 5:
            return !!state.formData.course;
        case 6:
            return !!state.formData.complaint_type;
        case 7:
            const ct = state.config?.complaint_types?.find(
                c => c.code === state.formData.complaint_type
            );
            if (ct?.requires_subject && !document.getElementById('subjectInput').value.trim()) {
                return false;
            }
            if (ct?.requires_teacher && !document.getElementById('teacherInput').value.trim()) {
                return false;
            }
            state.formData.subject_name = document.getElementById('subjectInput').value.trim();
            state.formData.teacher_name = document.getElementById('teacherInput').value.trim();
            return true;
        case 8:
            const msg = document.getElementById('messageInput').value.trim();
            if (!msg) {
                showError(t('enter_message') || 'Xabar kiriting');
                return false;
            }
            state.formData.message = msg;
            return true;
        default:
            return true;
    }
}

function prepareStep(stepNum) {
    switch (stepNum) {
        case 2:
            renderDirectionButtons();
            break;
        case 3:
            renderEduTypeButtons();
            break;
        case 4:
            renderEduLangButtons();
            break;
        case 5:
            renderCourseButtons();
            break;
        case 6:
            renderComplaintTypeButtons();
            break;
        case 7:
            prepareSubjectTeacherStep();
            break;
    }
}

function updateFormNav() {
    const backBtn = document.getElementById('backBtn');
    const nextBtn = document.getElementById('nextBtn');
    const submitBtn = document.getElementById('submitBtn');

    // Back button - always visible except step 1
    backBtn.style.display = state.currentStep > 1 ? 'flex' : 'none';

    // Next/Submit button
    if (state.currentStep === 8) {
        nextBtn.style.display = 'none';
        submitBtn.style.display = 'flex';
    } else {
        nextBtn.style.display = 'flex';
        submitBtn.style.display = 'none';
    }
}

// ============================================
// BUTTON RENDERERS
// ============================================
function renderFacultyButtons() {
    const container = document.getElementById('facultyButtons');
    container.innerHTML = '';

    state.config?.faculties?.forEach(faculty => {
        const btn = createOptionButton(
            t(faculty.translation_key) || faculty.code,
            () => selectFaculty(faculty.code)
        );
        container.appendChild(btn);
    });
}

async function renderDirectionButtons() {
    const container = document.getElementById('directionButtons');
    container.innerHTML = '<p>Yuklanmoqda...</p>';

    const data = await fetchDirections(state.formData.faculty);
    container.innerHTML = '';

    data.directions?.forEach(dir => {
        const btn = createOptionButton(
            t(dir.translation_key) || dir.code,
            () => selectDirection(dir.code)
        );
        container.appendChild(btn);
    });
}

function renderEduTypeButtons() {
    const container = document.getElementById('eduTypeButtons');
    container.innerHTML = '';

    state.config?.education_types?.forEach(et => {
        const btn = createOptionButton(
            t(et.translation_key) || et.code,
            () => selectEduType(et.code)
        );
        container.appendChild(btn);
    });
}

function renderEduLangButtons() {
    const container = document.getElementById('eduLangButtons');
    container.innerHTML = '';

    state.config?.education_languages?.forEach(el => {
        const btn = createOptionButton(
            t(el.translation_key) || el.code,
            () => selectEduLang(el.code)
        );
        container.appendChild(btn);
    });
}

function renderCourseButtons() {
    const container = document.getElementById('courseButtons');
    container.innerHTML = '';

    const courseType = state.formData.faculty === 'magistratura' ? 'magistr' : 'regular';
    const courses = state.config?.courses?.[courseType] || [];

    courses.forEach(course => {
        const btn = createOptionButton(
            t(course.translation_key) || course.code,
            () => selectCourse(course.code)
        );
        container.appendChild(btn);
    });
}

function renderComplaintTypeButtons() {
    const container = document.getElementById('complaintTypeButtons');
    container.innerHTML = '';

    state.config?.complaint_types?.forEach(ct => {
        const btn = createOptionButton(
            t(ct.translation_key) || ct.code,
            () => selectComplaintType(ct.code)
        );
        container.appendChild(btn);
    });
}

function prepareSubjectTeacherStep() {
    const ct = state.config?.complaint_types?.find(
        c => c.code === state.formData.complaint_type
    );

    const subjectField = document.getElementById('subjectField');
    const teacherField = document.getElementById('teacherField');

    subjectField.style.display = ct?.requires_subject ? 'block' : 'none';
    teacherField.style.display = ct?.requires_teacher ? 'block' : 'none';

    // Clear inputs
    document.getElementById('subjectInput').value = '';
    document.getElementById('teacherInput').value = '';
}

function createOptionButton(text, onClick) {
    const btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'option-btn';
    btn.textContent = text;
    btn.onclick = (e) => {
        // Remove selected class from siblings
        const parent = btn.parentElement;
        parent.querySelectorAll('.option-btn').forEach(b => b.classList.remove('selected'));
        btn.classList.add('selected');
        onClick(e);
    };
    return btn;
}

// ============================================
// SELECTION HANDLERS
// ============================================
function selectFaculty(code) {
    state.formData.faculty = code;
    highlightSelected('facultyButtons', code);
    nextStep();
}

function selectDirection(code) {
    state.formData.direction = code;
    highlightSelected('directionButtons', code);
    nextStep();
}

function selectEduType(code) {
    state.formData.education_type = code;
    highlightSelected('eduTypeButtons', code);
    nextStep();
}

function selectEduLang(code) {
    state.formData.education_language = code;
    highlightSelected('eduLangButtons', code);
    nextStep();
}

function selectCourse(code) {
    state.formData.course = code;
    highlightSelected('courseButtons', code);
    nextStep();
}

function selectComplaintType(code) {
    state.formData.complaint_type = code;
    highlightSelected('complaintTypeButtons', code);
    nextStep();
}

function highlightSelected(containerId, selectedCode) {
    const container = document.getElementById(containerId);
    container.querySelectorAll('.option-btn').forEach(btn => {
        btn.classList.remove('selected');
    });
    // The clicked button is highlighted via the selection flow
}

// ============================================
// FORM SUBMISSION
// ============================================
document.getElementById('complaintForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    if (!validateCurrentStep()) return;

    await submitComplaint(state.formData);
});

function resetForm() {
    initComplaintForm();
    showView('homeView');
}

// ============================================
// RULES & SURVEYS
// ============================================
function renderRulesList() {
    const container = document.getElementById('rulesList');
    container.innerHTML = '';

    // Rules from translations
    const ruleTypes = ['grading', 'exam', 'general'];
    ruleTypes.forEach(type => {
        const card = document.createElement('div');
        card.className = 'rule-card';
        card.onclick = () => showRuleDetail(type);

        const icons = { grading: '📊', exam: '📝', general: '📋' };
        card.innerHTML = `
            <span class="rule-icon">${icons[type]}</span>
            <div class="rule-info">
                <span class="rule-title">${t('btn_' + type)}</span>
            </div>
        `;
        container.appendChild(card);
    });
}

function showRuleDetail(type) {
    const modal = document.getElementById('ruleDetail');
    const title = document.getElementById('ruleTitle');
    const body = document.getElementById('ruleBody');

    title.textContent = t('btn_' + type);
    // In actual app, we'd have rules_grading translation
    body.innerHTML = t('rules_' + type).replace(/\n/g, '<br>');

    modal.style.display = 'flex';
}

function hideRuleDetail() {
    document.getElementById('ruleDetail').style.display = 'none';
}

function renderSurveyList() {
    const container = document.getElementById('surveyList');
    container.innerHTML = '';

    state.config?.surveys?.forEach(survey => {
        const card = document.createElement('a');
        card.className = 'survey-card';
        card.href = survey.url;
        card.target = '_blank';

        card.innerHTML = `
            <span class="survey-icon">📊</span>
            <div class="survey-info">
                <span class="survey-title">${t(survey.translation_key)}</span>
            </div>
        `;
        container.appendChild(card);
    });
}

// ============================================
// ADMIN LOGIC
// ============================================
async function loadAdminDashboard() {
    showLoading();
    try {
        const response = await fetch(`${API_BASE}/api/admin/dashboard`);
        const data = await response.json();

        document.getElementById('statsToday').textContent = data.today || 0;
        document.getElementById('statsWeek').textContent = data.week || 0;
        document.getElementById('statsMonth').textContent = data.month || 0;
    } catch (error) {
        console.error('Error loading dashboard:', error);
    } finally {
        hideLoading();
    }
}

async function showAdminSettings(type) {
    state.currentSettingType = type;
    showView('adminSettingsView');

    const titleEl = document.getElementById('settingsTitle');
    const titles = {
        admins: t('btn_manage_admins'),
        faculties: t('btn_manage_faculties'),
        directions: t('btn_manage_directions'),
        questions: t('btn_manage_questions'),
        translations: t('btn_manage_translations')
    };
    titleEl.textContent = titles[type] || type;

    loadSettingsList(type);
}

async function loadSettingsList(type) {
    const container = document.getElementById('settingsList');
    container.innerHTML = '<p>Yuklanmoqda...</p>';

    try {
        const response = await fetch(`${API_BASE}/api/admin/settings/${type}`);
        const data = await response.json();

        container.innerHTML = '';
        data.items?.forEach(item => {
            const el = document.createElement('div');
            el.className = 'settings-item';

            // Simplified display based on type
            let name = item[0] || 'Unknown';
            let detail = item[1] || '';

            if (type === 'admins') { name = item[1] || item[0]; detail = `ID: ${item[0]}`; }
            if (type === 'questions') { name = t(item[1]); detail = `Type: ${item[2]}`; }

            el.innerHTML = `
                <div class="settings-info">
                    <span class="settings-name">${name}</span>
                    <span class="settings-detail">${detail}</span>
                </div>
                <div class="settings-actions">
                    <button class="action-icon edit-icon"><i class="fas fa-edit"></i></button>
                    <button class="action-icon delete-icon"><i class="fas fa-trash"></i></button>
                </div>
            `;
            container.appendChild(el);
        });
    } catch (error) {
        container.innerHTML = '<p>Xatolik yuz berdi</p>';
    }
}

// ============================================
// RATING FORM (CORRECTED)
// ============================================
function initRatingForm() {
    state.ratingData = {
        step: 1,
        faculty: null,
        direction: null,
        course: null,
        edu_type: null,
        edu_lang: null,
        subject_name: '',
        teacher_name: '',
        ratings: {},
        comment: ''
    };
    renderRatingFacultyButtons();
    showRatingStep(1);
}

function showRatingStep(step) {
    state.ratingData.step = step;
    document.querySelectorAll('#ratingForm .form-step').forEach(s => s.classList.remove('active'));

    const stepEl = document.getElementById(`ratingStep${step}`);
    if (stepEl) stepEl.classList.add('active');

    // Nav logic
    document.getElementById('ratingBackBtn').style.display = step > 1 ? 'flex' : 'none';
    document.getElementById('ratingSubmitBtn').style.display = step === 9 ? 'flex' : 'none'; // Step 9 is submit
}

function renderRatingFacultyButtons() {
    const container = document.getElementById('ratingFacultyButtons');
    container.innerHTML = '';
    state.config?.faculties?.forEach(f => {
        const btn = createOptionButton(t(f.translation_key), () => {
            state.ratingData.faculty = f.code;
            nextRatingStep();
        });
        container.appendChild(btn);
    });
}

function nextRatingStep() {
    const next = state.ratingData.step + 1;
    const faculty = state.ratingData.faculty;

    // Skip education type/lang for magistratura
    if (faculty === 'magistratura') {
        if (state.ratingData.step === 2) { // If currently on direction step
            showRatingStep(5); // Skip to course selection
            renderRatingCourseButtons();
            return;
        }
    }

    if (next === 2) renderRatingDirectionButtons();
    else if (next === 3) renderRatingEduTypeButtons();
    else if (next === 4) renderRatingEduLangButtons();
    else if (next === 5) renderRatingCourseButtons();
    else if (next === 6) renderRatingSubjectStep();
    else if (next === 7) renderRatingTeacherStep();
    else if (next === 8) renderRatingQuestions();
    else if (next === 9) renderRatingCommentStep();

    showRatingStep(next);
}

async function renderRatingEduTypeButtons() {
    const container = getOrCreateRatingStepContainer('ratingStep3', 'choose_edu_type', 'ratingEduTypeButtons');
    container.innerHTML = '';
    state.config?.education_types?.forEach(et => {
        const btn = createOptionButton(t(et.translation_key), () => {
            state.ratingData.edu_type = et.code;
            nextRatingStep();
        });
        container.appendChild(btn);
    });
}

async function renderRatingEduLangButtons() {
    const container = getOrCreateRatingStepContainer('ratingStep4', 'choose_edu_lang', 'ratingEduLangButtons');
    container.innerHTML = '';
    state.config?.education_languages?.forEach(el => {
        const btn = createOptionButton(t(el.translation_key), () => {
            state.ratingData.edu_lang = el.code;
            nextRatingStep();
        });
        container.appendChild(btn);
    });
}

async function renderRatingCourseButtons() {
    const container = getOrCreateRatingStepContainer('ratingStep5', 'choose_course', 'ratingCourseButtons');
    container.innerHTML = '';
    const courseType = state.ratingData.faculty === 'magistratura' ? 'magistr' : 'regular';
    state.config?.courses?.[courseType]?.forEach(c => {
        const btn = createOptionButton(t(c.translation_key), () => {
            state.ratingData.course = c.code;
            nextRatingStep();
        });
        container.appendChild(btn);
    });
}

function renderRatingSubjectStep() {
    const container = getOrCreateRatingStepContainer('ratingStep6', 'enter_subject', 'ratingSubjectInput');
    container.innerHTML = `
        <input type="text" id="ratingSubject" class="form-input" placeholder="${t('enter_subject')}" onchange="state.ratingData.subject_name = this.value">
        <button class="nav-btn primary" onclick="nextRatingStep()">${t('btn_next')}</button>
    `;
}

function renderRatingTeacherStep() {
    const container = getOrCreateRatingStepContainer('ratingStep7', 'enter_teacher', 'ratingTeacherInput');
    container.innerHTML = `
        <input type="text" id="ratingTeacher" class="form-input" placeholder="${t('enter_teacher')}" onchange="state.ratingData.teacher_name = this.value">
        <button class="nav-btn primary" onclick="nextRatingStep()">${t('btn_next')}</button>
    `;
}

function renderRatingCommentStep() {
    // Already in HTML as step 7, but let's make it step 9
    const step7 = document.getElementById('ratingStep7');
    if (step7) step7.id = 'ratingStep9'; // Corrected ID to match the new step number
    // Ensure the content is correct for the comment step, assuming it's pre-existing in HTML
    // If not, it would need to be created similar to other steps.
}

function getOrCreateRatingStepContainer(stepId, titleKey, buttonsId) {
    let stepEl = document.getElementById(stepId);
    if (!stepEl) {
        stepEl = document.createElement('div');
        stepEl.id = stepId;
        stepEl.className = 'form-step';
        stepEl.innerHTML = `
            <label class="form-label" data-i18n="${titleKey}">${t(titleKey)}</label>
            <div id="${buttonsId}" class="button-group"></div>
        `;
        // Insert before the comment step, which is now ratingStep9
        document.getElementById('ratingForm').insertBefore(stepEl, document.getElementById('ratingStep9') || document.getElementById('ratingQuestionsStep'));
    }
    // If buttonsId is for an input, return the stepEl itself or the input container
    if (buttonsId.includes('Input')) {
        return stepEl;
    }
    return document.getElementById(buttonsId);
}

function renderRatingQuestions() {
    const container = document.getElementById('questionContainer');
    container.innerHTML = '';

    state.config?.rating_questions?.forEach(q => {
        const item = document.createElement('div');
        item.className = 'question-item';
        item.innerHTML = `
            <span class="question-text">${t(q.translation_key)}</span>
            <div class="rating-options" id="q_${q.number}">
                ${[1, 2, 3, 4, 5].map(n => `
                    <button class="rating-btn" onclick="setRating(${q.number}, ${n})">${n}</button>
                `).join('')}
            </div>
        `;
        container.appendChild(item);
    });
}

function prevRatingStep() {
    if (state.ratingData.step > 1) {
        showRatingStep(state.ratingData.step - 1);
    } else {
        showView('homeView');
    }
}

async function renderRatingDirectionButtons() {
    const container = document.getElementById('ratingDirectionButtons');
    if (!container) {
        // Create container if it doesn't exist in index.html (I should add it)
        const step2 = document.createElement('div');
        step2.id = 'ratingStep2';
        step2.className = 'form-step';
        step2.innerHTML = `
            <label class="form-label" data-i18n="choose_direction">Yo'nalishni tanlang</label>
            <div id="ratingDirectionButtons" class="button-group"></div>
        `;
        document.getElementById('ratingForm').insertBefore(step2, document.getElementById('ratingQuestionsStep'));
    }
    const target = document.getElementById('ratingDirectionButtons');
    target.innerHTML = '<p>Yuklanmoqda...</p>';
    const data = await fetchDirections(state.ratingData.faculty);
    target.innerHTML = '';
    data.directions?.forEach(dir => {
        const btn = createOptionButton(t(dir.translation_key), () => {
            state.ratingData.direction = dir.code;
            nextRatingStep();
        });
        target.appendChild(btn);
    });
}

// ============================================
// TRANSLATION FUNCTIONS
// ============================================
function t(key) {
    return state.translations[key] || key;
}

function applyTranslations() {
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        const translation = t(key);
        if (translation && translation !== key) {
            el.textContent = translation;
        }
    });
}

// ============================================
// UTILITY FUNCTIONS
// ============================================
function showLoading() {
    document.getElementById('loadingOverlay').classList.add('active');
}

function hideLoading() {
    document.getElementById('loadingOverlay').classList.remove('active');
}

function showError(message) {
    if (tg) {
        tg.showAlert(message);
    } else {
        alert(message);
    }
}

// ============================================
// INITIALIZATION
// ============================================
document.addEventListener('DOMContentLoaded', async () => {
    console.log('Mini App loading...');

    // Initialize Telegram
    initTelegram();

    // Fetch config
    await fetchConfig();

    console.log('Mini App ready!');
});

// Make functions globally available
window.showView = showView;
window.nextStep = nextStep;
window.prevStep = prevStep;
window.resetForm = resetForm;
window.showRuleDetail = showRuleDetail;
window.hideRuleDetail = hideRuleDetail;
window.toggleLangMenu = toggleLangMenu;
window.nextRatingStep = nextRatingStep;
window.prevRatingStep = prevRatingStep;
window.submitRating = submitRating;
window.setRating = setRating;
