# dash-grid-layout

Dash UI Component for using the React Grid Layout library

## Dash

Go to this link to learn about [Dash][].

## Getting started

```sh
# Install dependencies
$ npm install

# Watch source for changes and build to `lib/`
$ npm start
```

## Development

### Demo server

You can start up a demo development server to see a demo of the rendered
components:

```sh
$ builder run demo
$ open http://localhost:9000
```

You have to maintain the list of components in `demo/Demo.react.js`.

### Code quality and tests

#### To run lint and unit tests:

```sh
$ npm test
```

#### To run unit tests and watch for changes:

```sh
$ npm run test-watch
```

#### To debug unit tests in a browser (Chrome):

```sh
$ npm run test-debug
```

1. Wait until Chrome launches.
2. Click the "DEBUG" button in the top right corner.
3. Open up Chrome Devtools (`Cmd+opt+i`).
4. Click the "Sources" tab.
5. Find source files
  - Navigate to `webpack:// -> . -> spec/components` to find your test source files.
  - Navigate to `webpack:// -> [your/repo/path]] -> dash-grid-layout -> src` to find your component source files.
6. Now you can set breakpoints and reload the page to hit them.
7. The test output is available in the "Console" tab, or in any tab by pressing "Esc".

#### To run a specific test

In your test, append `.only` to a `describe` or `it` statement:

```javascript
describe.only('Foo component', () => {
    // ...
})l
```

### Testing your components in Dash

1. Build development bundle to `lib/` and watch for changes

        # Once this is started, you can just leave it running.
        $ npm start

2. Install module locally (after every change)

        # Generate metadata, and build the JavaScript bundle
        $ npm run install-local

        # Now you're done. For subsequent changes, if you've got `npm start`
        # running in a separate process, it's enough to just do:
        $ python setup.py install

3. Run the dash layout you want to test

        # Import dash-grid-layout to your layout, then run it:
        $ python my_dash_layout.py


**TODO:** There is a workflow that links your module into `site-packages` which would
make it unnecessary to re-run `2.` on every change: `python setup.py develop`.
Unfortunately, this doesn't seem to work with resources defined in
`package_data`.

See https://github.com/plotly/dash-components-archetype/issues/20


## Installing python package locally

Before publishing to PyPi, you can test installing the module locally:

```sh
# Install in `site-packages` on your machine
$ npm run install-local
```

## Uninstalling python package locally

```sh
$ npm run uninstall-local
```

## Publishing

For now, multiple steps are necessary for publishing to NPM and PyPi,
respectively. **TODO:**
[#5](https://github.com/plotly/dash-components-archetype/issues/5) will roll up
publishing steps into one workflow.

Ask @chriddyp to get NPM / PyPi package publishing accesss.

1. Preparing to publish to NPM

        # Bump the package version
        $ npm version major|minor|patch

        # Push branch and tags to repo
        $ git push --follow-tags

2. Preparing to publish to PyPi

        # Bump the PyPi package to the same version
        $ vi setup.py

        # Commit to github
        $ git add setup.py
        $ git commit -m "Bump pypi package version to vx.x.x"

3. Publish to npm and PyPi

        $ npm run publish-all

## Builder / Archetype

We use [Builder][] to centrally manage build configuration, dependencies, and
scripts.

To see all `builder` scripts available:

```sh
$ builder help
```

See the [dash-components-archetype][] repo for more information.


[Builder]: https://github.com/FormidableLabs/builder
[Dash]: https://github.com/plotly/dash2
[dash-components-archetype]: https://github.com/plotly/dash-components-archetype

# Component Documentation

## GridLayout

```
{
  /**
   * The ID used to identify the component in Dash callbacks
   */
  id: PropTypes.string,

  /**
   * A list of renderable child elements, that will be placed inside the
     grid
   */
  children: PropTypes.node,

  /**
   * The height, in pixels of a row in the grid
   */
  rowHeight: PropTypes.number,

  /**
   * The number of columns to display on the grid
   */
  cols: PropTypes.number,

  /**
   * The width, in pixels, of the grid
   */
  width: PropTypes.number,

  /**
   * If true, containers will automatically resize to fit the content
   */
  autoSize: PropTypes.bool,

  /**
   * CSS selector for tags that will not be draggable. Requires a
     leading '.'
   */
  draggableCancel: PropTypes.string,

  /**
   * CSS selector for tags that will act as the draggable handle.
     Requires a leading '.'
   */
  draggableHandle: PropTypes.string,

  /**
   * If true, the layout will compact vertically
   */
  verticalCompact: PropTypes.bool,

  /**
   * Compaction type.
   * One of 'vertical' and 'horizontal'
   */
  compactType: PropTypes.oneOf(['vertical', 'horizontal']),

  /**
   * Array of objects with the format:
   * { x: number, y: number, w: number, h: number }
   * If custom keys are used, then an optional `i` parameter can
   * be added that matches the key
   */
  layout: PropTypes.arrayOf(PropTypes.shape({
    x: PropTypes.number.isRequired,
    y: PropTypes.number.isRequired,
    w: PropTypes.number.isRequired,
    h: PropTypes.number.isRequired,
    i: PropTypes.Number
  })),

  /**
   * Margin between items [x, y] in px
   */
  margin: PropTypes.arrayOf(PropTypes.number),

  /**
   * Padding inside the container [x, y] in px
   */
  containerPadding: PropTypes.arrayOf(PropTypes.number),

  /**
   * Elements can be dragged
   */
  isDraggable: PropTypes.bool,

  /**
   * Elements can be resized
   */
  isResizable: PropTypes.bool,

  /**
   * Use CSS transforms instead of Position. Improves performance if
     switched on
   */
  useCSSTransforms: PropTypes.bool,

  /**
   * If true, grid items won't change position when being
   * dragged over
   */
  preventCollision: PropTypes.bool,

  /**
   * Callback upon the layout changed
   * @param layout: the layout
   */
  onLayoutChange: PropTypes.func,

  /**
   * Callback when dragging is started
   */
  onDragStart: PropTypes.func,

  /**
   * Callback upon each drag movement
   */
  onDrag: PropTypes.func,

  /**
   * Callback upon drag completion
   */
  onDragStop: PropTypes.func,

  /**
   * Calls when resize starts
   */
  onResizeStart: PropTypes.func,

  /**
   * Calls when resize movement happens
   */
  onResize: PropTypes.func,

  /**
   * Calls when resize is complete
   */
  onResizeStop: PropTypes.func,

  /**
   * Dash-assigned callback that should be called whenever any of the
     properties change
   */
  setProps: PropTypes.func
}
```

## GridItem

```
{
  /**
   * An identifier for the component.
   * Synonymous with `key`, but `key` cannot be specified as
   * a PropType without causing errors. A caveat to this is that when
     using
   * the component in pure React (as opposed to via Dash), both `i` and
     `key`
   * must be specified
   */
  i: PropTypes.string.isRequired,

  /**
   * A list of child elements to place inside the grid ite,
   */
  children: PropTypes.node,

  /**
   * An object describing the layout of the element
   */
  layout: PropTypes.shape({
    /**
     * The x-value of the element location, in grid units
     */
    x: PropTypes.number.isRequired,

    /**
     * The y-value of the element location, in grid units
     */
    y: PropTypes.number.isRequired,

    /**
     * The width of the element, in grid units
     */
    w: PropTypes.number.isRequired,

    /**
     * The height of the element, in grid units
     */
    h: PropTypes.number.isRequired,

    /**
     * The minimum width of the element, in grid units
     */
    minW: PropTypes.number,

    /**
     * The maximum width of the element, in grid units
     */
    maxW: PropTypes.number,

    /**
     * The minimum height of the element, in grid units
     */
    minH: PropTypes.number,

    /**
     * The maximum height of the element, in grid units
     */
    maxH: PropTypes.number,

    /**
     * Is static: if true, the element is not resizable or draggable
     */
    static: PropTypes.bool,

    /**
     * If false, element can not be dragged
     */
    isDraggable: PropTypes.bool,

    /**
     * If false, the element can not be resized
     */
    isResizable: PropTypes.bool
  }),


  /**
   * Dash-assigned callback that should be called whenever any of the
     properties change
   */
  setProps: PropTypes.func
}
```

See `usage.py` for example usage
