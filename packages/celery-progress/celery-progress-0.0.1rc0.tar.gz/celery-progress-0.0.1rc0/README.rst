Celery Progress Bars for Django
===============================

Drop in, dependency-free progress bars for your Django/Celery
applications.

Super simple setup. Lots of customization available.

Usage
-----

Recording Progress
~~~~~~~~~~~~~~~~~~

In your task you should add something like this:

.. code:: python

    from celery_progress.backend import ProgressRecorder

    @shared_task(bind=True)
    def my_task(self, seconds):
        progress_recorder = ProgressRecorder(self)
        for i in range(seconds):
            time.sleep(i)
            progress_recorder.set_progress(i, seconds)
        return 'done'

Displaying progress
~~~~~~~~~~~~~~~~~~~

In the view where you call the task you need to get the task ID like so:

**views.py**

.. code:: python

    def progress_view(request):
        result = my_task.delay(10)
        return render(request, 'display_progress.html', context={'task_id': task_id})

Then in the page you want to show the progress bar you just do the
following.

1. Add the following HTML wherever you want your progress bar to appear:

**display\_progress.html**

.. code:: html

    <div class='progress-wrapper'>
      <div id='progress-bar' class='progress-bar' style="background-color: #68a9ef; width: 0%;">&nbsp;</div>
    </div>
    <div id="progress-bar-message">Waiting for progress to start...</div>

2. Import the javascript file.

**display\_progress.html**

.. code:: html

    <script src="{% static 'celery_progress/celery_progress.js' %}"></script>

3. Initialize the progress bar:

.. code:: javascript

    // vanilla JS version
    var progressUrl = "{% url 'celery_progress:task_status' task_id %}";
    document.addEventListener("DOMContentLoaded", function () {
      CeleryProgressBar.initProgressBar(progressUrl);
    });

or

.. code:: javascript

    // JQuery
    var progressUrl = "{% url 'celery_progress:task_status' task_id %}";
    $(function () {
      CeleryProgressBar.initProgressBar(progressUrl)
    });

Customization
-------------

The ``initProgressBar`` function takes an optional object of options.
The following options are supported:

+-----------+-----------------+------------------+
| Option    | What it does    | Default Value    |
+===========+=================+==================+
| pollInter | How frequently  | 500              |
| val       | to poll for     |                  |
|           | progress (in    |                  |
|           | milliseconds)   |                  |
+-----------+-----------------+------------------+
| progressB | Override the ID | 'progress-bar'   |
| arId      | used for the    |                  |
|           | progress bar    |                  |
+-----------+-----------------+------------------+
| progressB | Override the ID | 'progress-bar-me |
| arMessage | used for the    | ssage'           |
| Id        | progress bar    |                  |
|           | message         |                  |
+-----------+-----------------+------------------+
| progressB | Override the    | document.getElem |
| arElement | *element* used  | entById(progress |
|           | for the         | BarId)           |
|           | progress bar.   |                  |
|           | If specified,   |                  |
|           | progressBarId   |                  |
|           | will be         |                  |
|           | ignored.        |                  |
+-----------+-----------------+------------------+
| progressB | Override the    | document.getElem |
| arMessage | *element* used  | entById(progress |
| Element   | for the         | BarMessageId)    |
|           | progress bar    |                  |
|           | message. If     |                  |
|           | specified,      |                  |
|           | progressBarMess |                  |
|           | ageId           |                  |
|           | will be         |                  |
|           | ignored.        |                  |
+-----------+-----------------+------------------+
| onProgres | function to     | CeleryProgressBa |
| s         | call when       | r.onProgressDefa |
|           | progress is     | ult              |
|           | updated         |                  |
+-----------+-----------------+------------------+
| onSuccess | function to     | CeleryProgressBa |
|           | call when       | r.onSuccessDefau |
|           | progress        | lt               |
|           | successfully    |                  |
|           | completes       |                  |
+-----------+-----------------+------------------+
| onError   | function to     | CeleryProgressBa |
|           | call when       | r.onErrorDefault |
|           | progress        |                  |
|           | completes with  |                  |
|           | an error        |                  |
+-----------+-----------------+------------------+
