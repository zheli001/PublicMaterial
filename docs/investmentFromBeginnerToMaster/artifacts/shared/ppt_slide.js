// Ruban Investment Vlog Shared Slide Navigation JS
(function() {
  const slides = document.querySelectorAll('.slide');
  let current = 0;
  function showSlide(idx) {
    slides.forEach((s, i) => s.classList.toggle('active', i === idx));
  }
  function nextSlide() {
    current = (current + 1) % slides.length;
    showSlide(current);
  }
  function prevSlide() {
    current = (current - 1 + slides.length) % slides.length;
    showSlide(current);
  }
  document.addEventListener('keydown', function(e) {
    if (e.key === 'ArrowLeft') prevSlide();
    if (e.key === 'ArrowRight') nextSlide();
  });
  showSlide(current);

  function applyPresentationConfig() {
    // Load configuration from embedded JSON
    var configScript = document.getElementById('lesson-config');
    var config = {
      title: '',
      subtitle: '',
      background: '',
      brand: '',
      headingFont: '',
      footerText: 'Ruban Investment Vlog © 2025 | Jeff Li | zheli001@gmail.com'
    };
    if (configScript) {
      try {
        var json = JSON.parse(configScript.textContent);
        Object.assign(config, json);
      } catch(e) {}
    }

    // Set document title
    if (config.title && config.subtitle) {
      document.title = config.title + ':' + config.subtitle;
    } else if (config.title) {
      document.title = config.title;
    }

    // Set background image if configured
    if (config.background) {
      document.body.style.backgroundImage = 'url(' + config.background + ')';
      document.body.style.backgroundSize = 'cover';
      document.body.style.backgroundPosition = 'center';
    }

    // Add brand image if configured
    if (config.brand) {
      var brandImg = document.createElement('img');
      brandImg.src = config.brand;
      brandImg.className = 'brand-logo';
      brandImg.style.position = 'absolute';
      brandImg.style.top = '32px';
      brandImg.style.left = '48px';
      brandImg.style.height = '3em';
      brandImg.style.width = '3em';
      brandImg.style.opacity = '0.9';
      brandImg.style.borderRadius = '50%'; // Make it round
      brandImg.style.objectFit = 'cover'; // Ensure image fills the circle
      brandImg.style.boxShadow = '0 2px 8px rgba(0,0,0,0.15)'; // Optional: subtle shadow
      document.body.appendChild(brandImg);
    }

    // Customize heading font if configured
    if (config.headingFont) {
      var heads = document.querySelectorAll('h1, h2, h3');
      heads.forEach(function(h) {
        h.style.fontFamily = config.headingFont;
      });
    }

    // Add footer text
    var footer = document.createElement('div');
    footer.className = 'slide-footer';
    footer.textContent = config.footerText || 'Ruban Investment Vlog © 2025 | Jeff Li | zheli001@gmail.com';
    footer.style.position = 'fixed';
    footer.style.bottom = '8px';
    footer.style.left = '0';
    footer.style.width = '100%';
    footer.style.textAlign = 'center';
    footer.style.color = '#888';
    footer.style.fontSize = '1em';
    footer.style.opacity = '0.85';
    document.body.appendChild(footer);
  }

  applyPresentationConfig();
})();
