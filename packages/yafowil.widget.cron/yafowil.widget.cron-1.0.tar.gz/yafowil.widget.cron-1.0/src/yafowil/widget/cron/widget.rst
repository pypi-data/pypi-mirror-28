Cron widget
===========

Load requirements::

    >>> import yafowil.loader
    >>> import yafowil.widget.cron
    >>> from yafowil.base import factory

Render widget::

    >>> widget = factory('cron', name='cronwidget')
    >>> widget()
    u'<div class="crontab widget" id="input-cronwidget">...</div>'

Render with JS config properties::

    >>> widget = factory(
    ...     'cron',
    ...     name='cronwidget',
    ...     props={
    ...         'lang': 'de',
    ...         'start_year': 2010,
    ...         'end_year': 2020
    ...     })
    >>> widget()
    u'<div class="crontab widget" 
    data-end_year=\'2020\' 
    data-lang=\'de\' 
    data-start_year=\'2010\' id="input-cronwidget">...</div>'

Base extraction::

    >>> data = widget.extract({})
    >>> data.printtree()
    <RuntimeData cronwidget, value=<UNSET>, extracted=<UNSET> at ...>
      <RuntimeData cronwidget.minute, value=<UNSET>, extracted=<UNSET> at ...>
      <RuntimeData cronwidget.hour, value=<UNSET>, extracted=<UNSET> at ...>
      <RuntimeData cronwidget.dom, value=<UNSET>, extracted=<UNSET> at ...>
      <RuntimeData cronwidget.month, value=<UNSET>, extracted=<UNSET> at ...>
      <RuntimeData cronwidget.dow, value=<UNSET>, extracted=<UNSET> at ...>
      <RuntimeData cronwidget.year, value=<UNSET>, extracted=<UNSET> at ...>

Valid widget extraction. Returns a datastructure, whic can be used with python-crontab::

    >>> request = {
    ...     'cronwidget.month': u'3,6,9,12',
    ...     'cronwidget.dom': u'1,15,30',
    ...     'cronwidget.hour': u'0,6,12,18',
    ...     'cronwidget.minute': u'0,10,20,30,40,50',
    ...     'cronwidget.dow': u'1,3,5',
    ...     'cronwidget.year': u'2017'
    ... }

    >>> data = widget.extract(request)
    >>> data.printtree()
    <RuntimeData cronwidget, value=<UNSET>, extracted='0,10,20,30,40,50 0,6,12,18 1,15,30 3,6,9,12 1,3,5 2017' at ...>
      <RuntimeData cronwidget.minute, value=<UNSET>, extracted=u'0,10,20,30,40,50' at ...>
      <RuntimeData cronwidget.hour, value=<UNSET>, extracted=u'0,6,12,18' at ...>
      <RuntimeData cronwidget.dom, value=<UNSET>, extracted=u'1,15,30' at ...>
      <RuntimeData cronwidget.month, value=<UNSET>, extracted=u'3,6,9,12' at ...>
      <RuntimeData cronwidget.dow, value=<UNSET>, extracted=u'1,3,5' at ...>
      <RuntimeData cronwidget.year, value=<UNSET>, extracted=u'2017' at ...>

    >>> value = data.extracted
    >>> value
    '0,10,20,30,40,50 0,6,12,18 1,15,30 3,6,9,12 1,3,5 2017'

Widget with value::

    >>> widget = factory('cron', name='cronwidget', value=value)
    >>> widget()
    u'...name="cronwidget.minute" type="hidden" value="0,10,20,30,40,50" 
    ...name="cronwidget.hour" type="hidden" value="0,6,12,18" 
    ...name="cronwidget.dom" type="hidden" value="1,15,30" 
    ...name="cronwidget.month" type="hidden" value="3,6,9,12" 
    ...name="cronwidget.dow" type="hidden" value="1,3,5" 
    ...name="cronwidget.year" type="hidden" value="2017"
    ...' 

    >>> data = widget.extract({})
    >>> data.printtree()
    <RuntimeData cronwidget, value='0,10,20,30,40,50 0,6,12,18 1,15,30 3,6,9,12 1,3,5 2017', extracted=<UNSET> at ...>
      <RuntimeData cronwidget.minute, value='0,10,20,30,40,50', extracted=<UNSET> at ...>
      <RuntimeData cronwidget.hour, value='0,6,12,18', extracted=<UNSET> at ...>
      <RuntimeData cronwidget.dom, value='1,15,30', extracted=<UNSET> at ...>
      <RuntimeData cronwidget.month, value='3,6,9,12', extracted=<UNSET> at ...>
      <RuntimeData cronwidget.dow, value='1,3,5', extracted=<UNSET> at ...>
      <RuntimeData cronwidget.year, value='2017', extracted=<UNSET> at ...>

    >>> data.extracted
    <UNSET>

    >>> request = {
    ...     'cronwidget.month': u'3,6',
    ...     'cronwidget.dom': u'1,15',
    ...     'cronwidget.hour': u'12,18',
    ...     'cronwidget.minute': u'0,10,20',
    ...     'cronwidget.dow': u'1',
    ...     'cronwidget.year': u'*'
    ... }

    >>> data = widget.extract(request)
    >>> data.printtree()
    <RuntimeData cronwidget, value='0,10,20,30,40,50 0,6,12,18 1,15,30 3,6,9,12 1,3,5 2017', extracted='0,10,20 12,18 1,15 3,6 1 *' at ...>
      <RuntimeData cronwidget.minute, value='0,10,20,30,40,50', extracted=u'0,10,20' at ...>
      <RuntimeData cronwidget.hour, value='0,6,12,18', extracted=u'12,18' at ...>
      <RuntimeData cronwidget.dom, value='1,15,30', extracted=u'1,15' at ...>
      <RuntimeData cronwidget.month, value='3,6,9,12', extracted=u'3,6' at ...>
      <RuntimeData cronwidget.dow, value='1,3,5', extracted=u'1' at ...>
      <RuntimeData cronwidget.year, value='2017', extracted=u'*' at ...>

    >>> data.extracted
    '0,10,20 12,18 1,15 3,6 1 *'

Widget in conjunction with hybrid blueprint::

    >>> value = '0,10,20,30,40,50 0,6,12,18 1,15,30 3,6,9,12 1,3,5 2017,2018,2019'
    >>> widget = factory(
    ...     'div:cron',
    ...     name='cronwidget',
    ...     value=value,
    ...     props={
    ...         'leaf': True,
    ...         'div.class': 'wrapper-div'
    ...     })
    >>> widget()
    u'<div class="wrapper-div"><div class="crontab widget" ...>...</div></div>'

    >>> request = {
    ...     'cronwidget.month': u'1',
    ...     'cronwidget.dom': u'2',
    ...     'cronwidget.hour': u'3',
    ...     'cronwidget.minute': u'4',
    ...     'cronwidget.dow': u'5',
    ...     'cronwidget.year': u'*'
    ... }

    >>> data = widget.extract(request)
    >>> data.printtree()
    <RuntimeData cronwidget, value='0,10,20,30,40,50 0,6,12,18 1,15,30 3,6,9,12 1,3,5 2017,2018,2019', extracted='4 3 2 1 5 *' at ...>
      <RuntimeData cronwidget.minute, value='0,10,20,30,40,50', extracted=u'4' at ...>
      <RuntimeData cronwidget.hour, value='0,6,12,18', extracted=u'3' at ...>
      <RuntimeData cronwidget.dom, value='1,15,30', extracted=u'2' at ...>
      <RuntimeData cronwidget.month, value='3,6,9,12', extracted=u'1' at ...>
      <RuntimeData cronwidget.dow, value='1,3,5', extracted=u'5' at ...>
      <RuntimeData cronwidget.year, value='2017,2018,2019', extracted=u'*' at ...>
