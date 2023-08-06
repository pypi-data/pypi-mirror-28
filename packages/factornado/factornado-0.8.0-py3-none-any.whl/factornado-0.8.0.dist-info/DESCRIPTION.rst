Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Description-Content-Type: UNKNOWN
Description: factornado
        ==========
        
        Factory for creating micro-services with tornado
        
        0.8
        ~~~
        - Reorganize processes so that they are all child of main process (853d6e8)
        - Create a `logger` submodule for simpler log configuration (fb2f20e)
        
        0.7
        ~~~
        - handlers.RequestHandler has now methods to parse args and kwargs (3c28e0f)
        - Todo and Do handlers push errors traceback to tasks server (5c49712)
        - Close properly AsyncHTTPClient in Heartbeat.post (a98317c)
        
        0.6
        ~~~
        - Proxy properly service error reason (5e50a20)
        - Avoid multiple task assignment when multithreading tasks example (0d3fa50)
        
        0.5
        ~~~
        - Method Application.get_host (7e63ec3)
        - Todo.todo_loop has been replaced by Todo.todo_list with different signature (16c684e)
        - New handlers.Log handler is set by default (e0d972d)
        - Callbacks are not only on POST methods (9b2fc96)
        
        0.4
        ~~~
        - Tasks handlers are incorporated into the library (in `factornado.tasks`)
        - All examples have a swagger attribute.
        
        0.3
        ~~~
        - Several example on how to use factornado
        - Tests based on these examples
        - application.WebMethod allows to pass headers
        - heartbeat reorganized to be asynchronous
        - possibility to stop the server
        - shortcut factornado.RequestHandler to tornado.web.RequestHandler
        
        0.2
        ~~~
        - Application object lets you run a server in a few lines
        - Todo and Do handler let you create periodicTasks in a few lines
        
        
        0.1
        ~~~
        - A first version
        
Keywords: microservices web tornado
Platform: UNKNOWN
Classifier: Programming Language :: Python :: 2.7
Classifier: Programming Language :: Python :: 3.4
Classifier: Programming Language :: Python :: 3.5
Classifier: License :: OSI Approved :: MIT License
Classifier: Development Status :: 5 - Production/Stable
