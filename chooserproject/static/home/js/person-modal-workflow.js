// Not sure about any of this, but used to work with wagtail-generic-choosers...

(() => {
  'use strict';

  const React = window.React;
  const Modifier = window.DraftJS.Modifier;
  const RichUtils = window.DraftJS.RichUtils;
  const EditorState = window.DraftJS.EditorState;

  const TooltipEntity = window.draftail.TooltipEntity;

  const global = globalThis;
  const $ = global.jQuery;

  const getPersonChooserConfig = () => {
    return {
      url: global.chooserUrls.personChooser,
      urlParams: {},
      // TODO: GENERIC_CHOOSER_MODAL_ONLOAD_HANDLERS worked with
      // wagtail-generic-choosers, but it's not clear how to use it with
      // Wagtail provided choosers.
      onload: global.GENERIC_CHOOSER_MODAL_ONLOAD_HANDLERS,
    };
  };

  const filterPersonEntityData = (entityType, data) => {
    return {
      edit_link: data.edit_link,
      string: data.string,
      id: data.id,
    };
  };

  class PersonModalWorkflowSource extends React.Component {
    constructor(props) {
      super(props);
      this.onChosen = this.onChosen.bind(this);
      this.onClose = this.onClose.bind(this);
    }

    componentDidMount() {
      const { onClose, entityType, entity, editorState } = this.props;
      const { url, urlParams, onload } = getPersonChooserConfig(entityType);

      $(document.body).on('hidden.bs.modal', this.onClose);

      // eslint-disable-next-line new-cap
      this.model_workflow = global.ModalWorkflow({
        url,
        urlParams,
        onload,
        responses: {
          chosen: this.onChosen,
        },
        onError: () => {
          // eslint-disable-next-line no-alert
          window.alert(global.wagtailConfig.STRINGS.SERVER_ERROR);
          onClose();
        },
      });
    }

    componentWillUnmount() {
      this.model_workflow = null;
      this.workflow = null;

      $(document.body).off('hidden.bs.modal', this.onClose);
    }

    onChosen(data) {
      const { editorState, entityType, onComplete } = this.props;

      const content = editorState.getCurrentContent();
      const selection = editorState.getSelection();

      const entityData = filterPersonEntityData(entityType, data);
      const mutability = "MUTABLE";
      const contentWithEntity = content.createEntity(entityType.type, mutability, entityData);
      const entityKey = contentWithEntity.getLastCreatedEntityKey();

      let nextState;

      const shouldReplaceText = data.prefer_this_title_as_link_text || selection.isCollapsed();

      if (shouldReplaceText) {
        // If there is a title attribute, use it, otherwise we inject the URL.
        const newText = data.string;
        const newContent = Modifier.replaceText(content, selection, newText, null, entityKey);
        nextState = EditorState.push(editorState, newContent, 'insert-characters');
      } else {
        nextState = RichUtils.toggleLink(editorState, selection, entityKey);
      }

      // IE11 crashes when rendering the new entity in contenteditable if the modal is still open.
      // Other browsers do not mind. This is probably a focus management problem.
      // From the user's perspective, this is all happening too fast to notice either way.
      if (this.workflow) {
        this.workflow.close();
      }

      onComplete(nextState);
    }

    onClose(e) {
      const { onClose } = this.props;
      e.preventDefault();

      onClose();
    }

    render() {
      return null;
    }
  }

  const PersonLink = props => {
    const { entityKey, contentState } = props;
    const data = contentState.getEntity(entityKey).getData();

    let icon = React.createElement(window.wagtail.components.Icon, {name: 'snippet'});
    let label = data.string || '';

    return React.createElement(TooltipEntity, {
      entityKey: props.entityKey,
      children: props.children,
      onEdit: props.onEdit,
      onRemove: props.onRemove,
      icon: icon,
      label: label
    });
  };

  window.draftail.registerPlugin({
    type: 'PERSON',
    source: PersonModalWorkflowSource,
    decorator: PersonLink,
  });

})();
