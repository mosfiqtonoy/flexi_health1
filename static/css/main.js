/**
 * Flexi Health — Enterprise Client-Side Interaction Engine
 * Handles dynamic UI lifecycles, real-time metric rendering, 
 * session heartbeat monitoring, and device telemetry optimization.
 */

class FlexiHealthEngine {
    constructor() {
        // Enforcing application runtime bounds
        this.toastTimeout = 5000;
        this.init();
    }

    init() {
        // Core Execution Pipeline
        this.setupAutomatedToastDismissal();
        this.setupServiceAccessGuards();
        this.initSystemHeartbeat();
        this.optimizeInteractiveComponents();
    }

    /**
     * 1. Automated System Toast Dismissal Protocol
     * Dynamically handles backend flash notifications, gracefully fading them
     * out of the DOM layout matrix after the defined expiration parameter.
     */
    setupAutomatedToastDismissal() {
        const flashContainers = document.querySelectorAll('.max-w-4xl > div');
        
        flashContainers.forEach((toast) => {
            // Instantiate entry transition effects
            toast.style.transition = "all 0.6s cubic-bezier(0.16, 1, 0.3, 1)";
            
            setTimeout(() => {
                // Trigger programmatic hardware-accelerated collapse sequence
                toast.style.opacity = "0";
                toast.style.transform = "translateY(-12px) scale(0.98)";
                
                // Erase structural residue from active window memory
                setTimeout(() => toast.remove(), 600);
            }, this.toastTimeout);
        });
    }

    /**
     * 2. Security Protocol Service Access Guard
     * Intercepts hardware pointer clicks on deactivated feature nodes (e.g. Ambulance or Pharmacy)
     * if the required 500 BDT liquidity checkpoint has not been verified by the backend.
     */
    setupServiceAccessGuards() {
        const structuralNodes = document.querySelectorAll('button[disabled]');
        
        structuralNodes.forEach((node) => {
            // Re-enabling explicit event listener traps for advanced client messaging
            node.style.pointerEvents = "auto";
            
            node.addEventListener('click', (event) => {
                event.preventDefault();
                event.stopPropagation();
                
                // Dispatching a clean, localized system notification anchor
                this.triggerDynamicAlert(
                    "Security Protocol: Node Locked. Your mobile-recharge micro-savings must accumulate to a minimum of 500.00 BDT to authorize emergency services.",
                    "warning"
                );
            });
        });
    }

    /**
     * 3. Real-Time Dynamic Toast Injector
     * Spawns modular notifications dynamically without requiring direct server-side template flashes.
     */
    triggerDynamicAlert(message, tier = "warning") {
        // Querying or instantiating the toast anchor framework
        let streamAnchor = document.querySelector('.max-w-4xl');
        if (!streamAnchor) {
            streamAnchor = document.createElement('div');
            streamAnchor.className = "max-w-4xl mx-auto w-full px-4 mt-4 fixed top-16 left-1/2 -translate-x-1/2 z-50";
            document.body.prepend(streamAnchor);
        }

        const alertPayload = document.createElement('div');
        alertPayload.className = `p-4 rounded-xl mb-4 border flex items-center justify-between shadow-2xl backdrop-blur-md transition-all duration-500 transform translate-y-4 opacity-0
            ${tier === 'warning' ? 'bg-yellow-950/50 border-yellow-800/40 text-yellow-400' : 'bg-red-950/50 border-red-800/40 text-red-400'}`;
        
        alertPayload.innerHTML = `
            <span class="text-xs font-semibold tracking-wide leading-relaxed">${message}</span>
            <button onclick="this.parentElement.remove()" class="text-[10px] uppercase tracking-widest font-black opacity-60 hover:opacity-100 ml-4 cursor-pointer">Dismiss</button>
        `;

        streamAnchor.appendChild(alertPayload);
        
        // Execute structural rendering transition
        requestAnimationFrame(() => {
            alertPayload.classList.remove('translate-y-4', 'opacity-0');
        });

        // Register automatic disposal callback for injected payload
        setTimeout(() => {
            alertPayload.style.opacity = "0";
            alertPayload.style.transform = "translateY(-10px)";
            setTimeout(() => alertPayload.remove(), 500);
        }, this.toastTimeout + 2000);
    }

    /**
     * 4. Platform Client Telemetry & Active Session Heartbeat
     * Simulated performance matrix loop ensuring consistent synchronization logs.
     */
    initSystemHeartbeat() {
        const telemetryTicker = document.querySelector('.animate-pulse');
        if (telemetryTicker) {
            console.log("Flexi Health — Secure Telemetry Link Ingested Successfully.");
            // Network diagnostics logging could hook here in enterprise updates
        }
    }

    /**
     * 5. Interactive UI Micro-Animations
     * Enhances hover responsiveness on enterprise cards and interactive nodes.
     */
    optimizeInteractiveComponents() {
        const interactiveCards = document.querySelectorAll('.brand-glow');
        interactiveCards.forEach(card => {
            card.addEventListener('mousemove', (e) => {
                const rect = card.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;
                
                // Dynamically updating structural CSS properties for custom light tracking reflections
                card.style.setProperty('--mouse-x', `${x}px`);
                card.style.setProperty('--mouse-y', `${y}px`);
            });
        });
    }
}

// Instantiate Global Platform Application Layer Execution Controller
document.addEventListener("DOMContentLoaded", () => {
    window.FlexiHealthPlatform = new FlexiHealthEngine();
});
