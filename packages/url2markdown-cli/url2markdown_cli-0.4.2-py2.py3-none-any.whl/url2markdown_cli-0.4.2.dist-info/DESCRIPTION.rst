# url2markdown-cli

Fetch a url and translate it to markdown in one command.

## Usage

To install:

```shell
$ pip install url2markdown-cli
```

To use:

```shell
url2markdown --with-cache https://www.djangoproject.com/
```

To use your own custom url2markdown server instance (you should):

```shell
export URL2MARKDOWN_URL='http://markdownplease.com/?url={url}'
```

## Thanks

Thanks to @kennethreitz for his [url2markdown](https://github.com/kennethreitz/url2markdown) project which this compliments.

## Contact / Social Media

Here are a few ways to keep up with me online. If you have a question about this project, please consider opening a GitHub Issue.

[![](https://jefftriplett.com/assets/images/social/github.png)](https://github.com/jefftriplett)
[![](https://jefftriplett.com/assets/images/social/globe.png)](https://jefftriplett.com/)
[![](https://jefftriplett.com/assets/images/social/twitter.png)](https://twitter.com/webology)
[![](https://jefftriplett.com/assets/images/social/docker.png)](https://hub.docker.com/u/jefftriplett/)


## History

### 0.4.2 (2017-01-22)

- Re-factors app structure

### 0.4.1 (2017-01-22)

- Fixes README and HISTORY (oops)

### 0.4.0 (2017-01-22)

- Update to use markdownplease.com
- Update requests-cache to be optional

### 0.2.1 (2015-01-11)

- Updated readme to fix file path.

### 0.2.0 (2015-01-11)

- Renamed module.

### 0.1.0 (2015-01-11)

- First release on PyPI.


