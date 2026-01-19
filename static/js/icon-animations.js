// Advanced Icon Animation System
class IconAnimator {
    constructor() {
        this.animatedIcons = new Set();
        this.observer = null;
        this.init();
    }

    init() {
        this.setupIntersectionObserver();
        this.loadLottieIcons();
        this.setupHoverAnimations();
    }

    setupIntersectionObserver() {
        this.observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    this.animateIcon(entry.target);
                }
            });
        }, { threshold: 0.1 });

        // Observe all animatable icons
        document.querySelectorAll('[data-icon-animation]').forEach(icon => {
            this.observer.observe(icon);
        });
    }

    animateIcon(iconElement) {
        const animationType = iconElement.getAttribute('data-icon-animation');
        
        if (this.animatedIcons.has(iconElement)) return;
        this.animatedIcons.add(iconElement);

        switch (animationType) {
            case 'morph':
                this.morphAnimation(iconElement);
                break;
            case 'float':
                this.floatAnimation(iconElement);
                break;
            case 'pulse':
                this.pulseAnimation(iconElement);
                break;
            case 'spin':
                this.spinAnimation(iconElement);
                break;
            case 'bounce':
                this.bounceAnimation(iconElement);
                break;
            case 'wave':
                this.waveAnimation(iconElement);
                break;
            case 'orbit':
                this.orbitAnimation(iconElement);
                break;
            case 'particles':
                this.particlesAnimation(iconElement);
                break;
            default:
                this.defaultAnimation(iconElement);
        }
    }

    // Morphing animation (SVG path morphing)
    morphAnimation(iconElement) {
        const paths = iconElement.querySelectorAll('path');
        paths.forEach((path, index) => {
            const length = path.getTotalLength();
            path.style.strokeDasharray = length;
            path.style.strokeDashoffset = length;
            
            anime({
                targets: path,
                strokeDashoffset: [length, 0],
                duration: 800,
                delay: index * 100,
                easing: 'easeOutCubic',
                complete: function() {
                    path.style.strokeDasharray = 'none';
                }
            });
        });
    }

    // Floating animation
    floatAnimation(iconElement) {
        anime({
            targets: iconElement,
            translateY: [-10, 0],
            opacity: [0, 1],
            duration: 1000,
            easing: 'easeOutCubic'
        });
    }

    // Pulsing animation
    pulseAnimation(iconElement) {
        anime({
            targets: iconElement,
            scale: [0.8, 1],
            opacity: [0, 1],
            duration: 600,
            easing: 'easeOutCubic'
        });

        // Continuous gentle pulse
        setInterval(() => {
            anime({
                targets: iconElement,
                scale: [1, 1.05, 1],
                duration: 2000,
                easing: 'easeInOutSine'
            });
        }, 3000);
    }

    // Spinning animation
    spinAnimation(iconElement) {
        anime({
            targets: iconElement,
            rotate: {
                value: 360,
                duration: 2000,
                easing: 'easeInOutSine'
            },
            scale: [0, 1],
            opacity: [0, 1],
            duration: 800
        });
    }

    // Bouncing animation
    bounceAnimation(iconElement) {
        anime({
            targets: iconElement,
            translateY: [
                { value: -30, duration: 300, easing: 'easeOutSine' },
                { value: 0, duration: 300, easing: 'easeInSine' }
            ],
            opacity: [0, 1],
            scale: [0.8, 1],
            duration: 600
        });
    }

    // Wave animation for multiple elements
    waveAnimation(iconElement) {
        const children = iconElement.querySelectorAll('*');
        children.forEach((child, index) => {
            anime({
                targets: child,
                translateY: [-20, 0],
                opacity: [0, 1],
                duration: 500,
                delay: index * 100,
                easing: 'easeOutCubic'
            });
        });
    }

    // Orbiting animation
    orbitAnimation(iconElement) {
        const orbitContainer = document.createElement('div');
        orbitContainer.className = 'orbit-container';
        orbitContainer.style.position = 'relative';
        orbitContainer.style.display = 'inline-block';
        
        iconElement.parentNode.insertBefore(orbitContainer, iconElement);
        orbitContainer.appendChild(iconElement);

        // Create orbiting dots
        for (let i = 0; i < 3; i++) {
            const dot = document.createElement('div');
            dot.className = 'orbit-dot';
            dot.style.cssText = `
                position: absolute;
                width: 4px;
                height: 4px;
                background: #3B82F6;
                border-radius: 50%;
                top: 50%;
                left: 50%;
            `;
            orbitContainer.appendChild(dot);

            anime({
                targets: dot,
                rotate: 360,
                duration: 2000 + i * 500,
                loop: true,
                easing: 'linear'
            });
        }
    }

    // Particles animation
    particlesAnimation(iconElement) {
        const rect = iconElement.getBoundingClientRect();
        const particlesContainer = document.createElement('div');
        particlesContainer.className = 'particles-container';
        particlesContainer.style.cssText = `
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
        `;
        
        iconElement.style.position = 'relative';
        iconElement.appendChild(particlesContainer);

        for (let i = 0; i < 8; i++) {
            const particle = document.createElement('div');
            particle.className = 'icon-particle';
            particle.style.cssText = `
                position: absolute;
                width: 3px;
                height: 3px;
                background: #3B82F6;
                border-radius: 50%;
                top: 50%;
                left: 50%;
            `;

            particlesContainer.appendChild(particle);

            anime({
                targets: particle,
                translateX: () => anime.random(-30, 30),
                translateY: () => anime.random(-30, 30),
                opacity: [1, 0],
                scale: [1, 2],
                duration: 1000,
                delay: i * 100,
                easing: 'easeOutCubic'
            });
        }
    }

    // Default animation
    defaultAnimation(iconElement) {
        anime({
            targets: iconElement,
            scale: [0, 1],
            rotate: [-180, 0],
            opacity: [0, 1],
            duration: 800,
            easing: 'easeOutBack'
        });
    }

    // Lottie animations loader
    loadLottieIcons() {
        if (typeof lottie !== 'undefined') {
            document.querySelectorAll('[data-lottie-icon]').forEach(container => {
                const animationPath = container.getAttribute('data-lottie-icon');
                lottie.loadAnimation({
                    container: container,
                    renderer: 'svg',
                    loop: true,
                    autoplay: true,
                    path: animationPath
                });
            });
        }
    }

    // Hover animations setup
    setupHoverAnimations() {
        document.querySelectorAll('[data-hover-animation]').forEach(icon => {
            icon.addEventListener('mouseenter', () => {
                this.triggerHoverAnimation(icon);
            });
        });
    }

    triggerHoverAnimation(iconElement) {
        const animationType = iconElement.getAttribute('data-hover-animation');
        
        switch (animationType) {
            case 'wobble':
                this.wobbleHover(iconElement);
                break;
            case 'magnetic':
                this.magneticHover(iconElement);
                break;
            case 'ripple':
                this.rippleHover(iconElement);
                break;
            case 'glow':
                this.glowHover(iconElement);
                break;
            default:
                this.defaultHover(iconElement);
        }
    }

    wobbleHover(iconElement) {
        anime({
            targets: iconElement,
            rotate: [-5, 5, -3, 3, 0],
            duration: 600,
            easing: 'easeInOutSine'
        });
    }

    magneticHover(iconElement) {
        iconElement.addEventListener('mousemove', (e) => {
            const rect = iconElement.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            
            const moveX = (x - centerX) * 0.1;
            const moveY = (y - centerY) * 0.1;
            
            anime({
                targets: iconElement,
                translateX: moveX,
                translateY: moveY,
                duration: 300,
                easing: 'easeOutQuad'
            });
        });

        iconElement.addEventListener('mouseleave', () => {
            anime({
                targets: iconElement,
                translateX: 0,
                translateY: 0,
                duration: 500,
                easing: 'easeOutElastic'
            });
        });
    }

    rippleHover(iconElement) {
        const ripple = document.createElement('div');
        ripple.style.cssText = `
            position: absolute;
            border-radius: 50%;
            background: rgba(59, 130, 246, 0.3);
            transform: scale(0);
            pointer-events: none;
        `;
        
        iconElement.style.position = 'relative';
        iconElement.appendChild(ripple);

        const rect = iconElement.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        
        ripple.style.width = `${size}px`;
        ripple.style.height = `${size}px`;
        ripple.style.left = '0';
        ripple.style.top = '0';

        anime({
            targets: ripple,
            scale: [0, 2],
            opacity: [0.5, 0],
            duration: 600,
            easing: 'easeOutCubic',
            complete: () => ripple.remove()
        });
    }

    glowHover(iconElement) {
        anime({
            targets: iconElement,
            boxShadow: [
                '0 0 0px rgba(59, 130, 246, 0)',
                '0 0 20px rgba(59, 130, 246, 0.6)',
                '0 0 0px rgba(59, 130, 246, 0)'
            ],
            duration: 1000,
            easing: 'easeOutSine'
        });
    }

    defaultHover(iconElement) {
        anime({
            targets: iconElement,
            scale: 1.1,
            duration: 300,
            easing: 'easeOutBack'
        });

        iconElement.addEventListener('mouseleave', () => {
            anime({
                targets: iconElement,
                scale: 1,
                duration: 300,
                easing: 'easeOutBack'
            });
        });
    }
}

// Initialize icon animator when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    window.iconAnimator = new IconAnimator();
});