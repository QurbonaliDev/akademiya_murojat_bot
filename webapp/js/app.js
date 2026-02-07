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
    formData: {
        faculty: null,
        direction: null,
        education_type: null,
        education_language: null,
        course: null,
        complaint_type: null,
        subject_name: '',
        teacher_name: '',
        message: ''
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
        console.log('Config loaded:', state.config);
    } catch (error) {
        console.error('Error fetching config:', error);
        showError('Ma\'lumotlarni yuklashda xatolik');
    } finally {
        hideLoading();
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
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (result.success) {
            showView('successView');
            if (tg) {
                tg.showAlert('Murojaatingiz muvaffaqiyatli yuborildi!');
            }
        } else {
            showError(result.error || 'Xatolik yuz berdi');
        }
    } catch (error) {
        console.error('Error submitting complaint:', error);
        showError('Yuborishda xatolik');
    } finally {
        hideLoading();
    }
}

// ============================================
// VIEW NAVIGATION
// ============================================
function showView(viewId) {
    // Hide all views
    document.querySelectorAll('.view').forEach(view => {
        view.classList.remove('active');
    });

    // Show selected view
    const view = document.getElementById(viewId);
    if (view) {
        view.classList.add('active');
        state.currentView = viewId;
    }

    // Update header
    updateHeader(viewId);

    // Reset form when entering complaint view
    if (viewId === 'complaintView') {
        initComplaintForm();
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
    btn.onclick = onClick;
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
// RULES FUNCTIONS
// ============================================
function showRuleDetail(ruleType) {
    // For now, just show an alert with rule info
    if (tg) {
        tg.showAlert(`${ruleType} qoidalari haqida ma'lumot tez orada qo'shiladi!`);
    } else {
        alert(`${ruleType} qoidalari`);
    }
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
