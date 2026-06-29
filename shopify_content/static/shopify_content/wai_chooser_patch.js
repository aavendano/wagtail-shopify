(function () {
  function collectFormContent() {
    const form = document.querySelector('[data-edit-form]');
    if (!form) {
      return '';
    }

    const chunks = [];
    const add = (value) => {
      const text = (value || '').trim();
      if (text) {
        chunks.push(text);
      }
    };

    ['id_title', 'id_seo_title', 'id_search_description'].forEach((id) => {
      const el = form.querySelector(`#${id}`);
      if (el) {
        add(el.value);
      }
    });

    form.querySelectorAll('textarea, input[type="text"]').forEach((el) => {
      if (el.name && !el.name.includes('semantic_links')) {
        add(el.value);
      }
    });

    form.querySelectorAll('[contenteditable="true"]').forEach((el) => {
      add(el.innerText);
    });

    return chunks.join('\n\n');
  }

  async function fetchSuggestions(controller) {
    const formContent = collectFormContent();
    if (!formContent) {
      throw new Error('Unable to get page content for analysis.');
    }

    let limit = controller.limitValue;
    const maxForms = controller.panelComponent.opts.maxForms;
    if (maxForms) {
      limit = Math.min(maxForms - controller.panelComponent.getChildCount(), limit);
    }

    const exclude = [
      controller.instancePkValue,
      ...controller.seenPksValue,
      ...controller.getFormsetChildIds(),
    ].filter(Boolean);

    const response = await fetch(controller.urlValue, {
      method: 'POST',
      headers: {
        [wagtailConfig.CSRF_HEADER_NAME]: wagtailConfig.CSRF_TOKEN,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        arguments: {
          vector_index: controller.vectorIndexValue,
          exclude_pks: exclude,
          content: formContent,
          limit,
          chunk_size: controller.hasChunkSizeValue ? controller.chunkSizeValue : undefined,
        },
      }),
      signal: controller.abortController?.signal,
    });

    if (!response.ok) {
      throw new Error(`Error fetching AI response: ${response.status} ${response.statusText}`);
    }

    const payload = await response.json();
    return payload.data;
  }

  function patchControllerInstance(controller) {
    if (!controller || controller._waiSuggestionsPatched) {
      return false;
    }
    controller.getSuggestions = function () {
      return fetchSuggestions(this);
    };
    controller._waiSuggestionsPatched = true;
    return true;
  }

  function patchRegisteredControllers() {
    const app = window.wagtail?.app;
    if (!app || typeof app.getControllerForElementAndIdentifier !== 'function') {
      return;
    }
    document.querySelectorAll('[data-controller~="wai-chooser-panel"]').forEach((element) => {
      try {
        patchControllerInstance(
          app.getControllerForElementAndIdentifier(element, 'wai-chooser-panel'),
        );
      } catch (error) {
        // ignore
      }
    });
  }

  function installPatch() {
    const app = window.wagtail?.app;
    if (!app || app._waiChooserPatched) {
      return;
    }

    const originalRegister = app.register.bind(app);
    app.register = function (name, Controller) {
      if (name === 'wai-chooser-panel') {
        const originalConnect = Controller.prototype.connect;
        Controller.prototype.connect = function () {
          patchControllerInstance(this);
          if (originalConnect) {
            return originalConnect.call(this);
          }
        };
        Controller.prototype.getSuggestions = function () {
          return fetchSuggestions(this);
        };
        Controller.prototype.getSuggestions._waiSuggestionsPatched = true;
      }
      return originalRegister(name, Controller);
    };
    app._waiChooserPatched = true;
  }

  installPatch();
  document.addEventListener('DOMContentLoaded', () => {
    installPatch();
    patchRegisteredControllers();
  });
  document.addEventListener('w-unsaved:ready', patchRegisteredControllers);
})();
