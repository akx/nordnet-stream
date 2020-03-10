nordnet-stream
==============

Streams values from Nordnet's web sockets.

Caveat
------

Using this thing may be against Nordnet's T&C; I didn't read them with a fine enough comb to figure out the case.
However, the behavior of the websocket client here is more or less exactly what your web browser would do when browsing
the site (aside from very non-graceful connection closure).

As prescribed by the license, too,

> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
> IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
> FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
> AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
> LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
> OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
> SOFTWARE.

Now that that's out of the way...

Usage
-----

* Python 3.7 required (`async` ahoy!).
* Install requirements into a virtualenv.
* Set the `NEXT_COOKIE` envvar to the value (leading octothorpe included) of the `NEXT=` cookie you have
  in your Nordnet session.
* Run `python nstream_chart_client.py 17085951`, where `17085951` is the ID of the instrument
  to track; you can see it in the URL, e.g. `https://www.nordnet.fi/markkinakatsaus/something/17085951-something`.


