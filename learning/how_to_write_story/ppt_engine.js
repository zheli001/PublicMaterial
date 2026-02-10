import slidesData from './slides.js';

class PPTController {
    constructor() {
        this.currentSlideIndex = 0;
        this.container = document.getElementById('slide-container');
        this.progressBar = document.getElementById('progress-bar');

        this.init();
    }

    init() {
        this.renderSlide();
        this.setupEventListeners();
        this.updateProgress();
    }

    setupEventListeners() {
        document.addEventListener('keydown', (e) => {
            if (e.key === 'ArrowRight' || e.key === ' ') this.next();
            if (e.key === 'ArrowLeft') this.prev();
        });

        // Touch support for mobile/tablets
        let touchstartX = 0;
        let touchendX = 0;

        document.addEventListener('touchstart', e => {
            touchstartX = e.changedTouches[0].screenX;
        }, false);

        document.addEventListener('touchend', e => {
            touchendX = e.changedTouches[0].screenX;
            if (touchendX < touchstartX - 50) this.next();
            if (touchendX > touchstartX + 50) this.prev();
        }, false);
    }

    renderSlide() {
        const slide = slidesData[this.currentSlideIndex];
        this.container.innerHTML = '';
        this.container.className = `slide-content layout-${slide.layout}`;

        if (slide.background) {
            document.body.style.background = slide.background;
        } else {
            document.body.style.background = '#F0F4F8'; // Neutral default
        }

        const template = this.getTemplate(slide);
        this.container.innerHTML = template;

        // Add fade-in effect
        this.container.classList.remove('fade-in');
        void this.container.offsetWidth; // Trigger reflow
        this.container.classList.add('fade-in');
    }

    getTemplate(slide) {
        switch (slide.layout) {
            case 'title':
                return `
                    <div class="hero">
                        <h1 class="slide-title huge">${slide.title}</h1>
                        <p class="slide-subtitle">${slide.subtitle}</p>
                        <div class="decorative-line"></div>
                    </div>
                `;
            case 'concept':
                return `
                    <h2 class="slide-title">${slide.title}</h2>
                    <ul class="bullet-list">
                        ${slide.bullets.map(b => `<li>${this.formatMarkdown(b)}</li>`).join('')}
                    </ul>
                `;
            case 'interactive':
                return `
                    <div class="interactive-grid">
                        <div class="col-instructions">
                            <h2 class="slide-title">${slide.title}</h2>
                            <p class="context-text">${slide.instructions}</p>
                        </div>
                        <div class="col-task">
                            <div class="task-card">
                                <h3>🎯 Your Task</h3>
                                <p>${slide.task}</p>
                                <div class="hint"><strong>Tip:</strong> ${slide.hint}</div>
                            </div>
                        </div>
                    </div>
                `;
            case 'code':
                return `
                    <h2 class="slide-title">${slide.title}</h2>
                    <div class="code-block-container">
                        <pre><code>${slide.code}</code></pre>
                        <button class="copy-btn" onclick="navigator.clipboard.writeText('${slide.code}')">Copy Magic Phrase</button>
                    </div>
                    <p class="code-desc">${slide.description}</p>
                `;
            default:
                return `<h1>Slide layout ${slide.layout} not found</h1>`;
        }
    }

    formatMarkdown(text) {
        // Simple bold parser
        return text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    }

    next() {
        if (this.currentSlideIndex < slidesData.length - 1) {
            this.currentSlideIndex++;
            this.renderSlide();
            this.updateProgress();
        }
    }

    prev() {
        if (this.currentSlideIndex > 0) {
            this.currentSlideIndex--;
            this.renderSlide();
            this.updateProgress();
        }
    }

    updateProgress() {
        const percent = ((this.currentSlideIndex + 1) / slidesData.length) * 100;
        this.progressBar.style.width = `${percent}%`;
    }
}

window.addEventListener('DOMContentLoaded', () => {
    new PPTController();
});
