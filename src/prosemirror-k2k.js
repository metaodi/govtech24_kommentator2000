(function (prosemirrorModel, prosemirrorTransform, prosemirrorCommands, prosemirrorKeymap, prosemirrorState, prosemirrorView, prosemirrorHistory) {
  'use strict';

  // noteSchema{
  const noteSchema = new prosemirrorModel.Schema({
    nodes: {
      text: {},
      article: {
        content: "(num | heading | akn_paragraph)+",
        toDOM() { return ["article", 0] },
        parseDOM: [{ tag: "article" }]
      },
      num: {
        content: "bold",
        toDOM() { return ["num", 0] },
        parseDOM: [{ tag: "num" }]
      },
      bold: {
        content: "text*",
        toDOM() { return ["b", 0] },
        parseDOM: [{ tag: "b" }]
      },
      heading: {
        content: "text*",
        toDOM() { return ["heading", 0] },
        parseDOM: [{ tag: "heading" }]
      },
      akn_paragraph: {
        content: "content",
        toDOM() { return ["paragraph", 0] },
        parseDOM: [{ tag: "paragraph" }]
      },
      content: {
        content: "paragraph",
        toDOM() { return ["content", 0] },
        parseDOM: [{ tag: "content" }]
      },
      paragraph: {
        content: "text*",
        toDOM() { return ["p", 0] },
        parseDOM: [{ tag: "p" }]
      },
      doc: {
        content: "article+"
      }
    }
  });

  function makeNoteGroup(state, dispatch) {
    // Get a range around the selected blocks
    let range = state.selection.$from.blockRange(state.selection.$to);
    // See if it is possible to wrap that range in a note group
    let wrapping = prosemirrorTransform.findWrapping(range, noteSchema.nodes.notegroup);
    // If not, the command doesn't apply
    if (!wrapping) return false
    // Otherwise, dispatch a transaction, using the `wrap` method to
    // create the step that does the actual wrapping.
    if (dispatch) dispatch(state.tr.wrap(range, wrapping).scrollIntoView());
    return true
  }
  // }

  let histKeymap = prosemirrorKeymap.keymap({ "Mod-z": prosemirrorHistory.undo, "Mod-y": prosemirrorHistory.redo });

  function start(place, content, schema, plugins = []) {
    let doc = prosemirrorModel.DOMParser.fromSchema(schema).parse(content);
    return new prosemirrorView.EditorView(place, {
      state: prosemirrorState.EditorState.create({
        doc,
        plugins: plugins.concat([histKeymap, prosemirrorKeymap.keymap(prosemirrorCommands.baseKeymap), prosemirrorHistory.history()])
      })
    })
  }

  function id(str) { return document.getElementById(str) }

  start(id("k2k-editor"), id("k2k-content"), noteSchema, [prosemirrorKeymap.keymap({ "Ctrl-Space": makeNoteGroup })]);

})(PM.model, PM.transform, PM.commands, PM.keymap, PM.state, PM.view, PM.history);

