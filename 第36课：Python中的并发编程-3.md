## 第36课：Python中的并发编程-3

爬虫是典型的 I/O 密集型任务。



**I/O密集型任务**是指那些需要大量输入/输出操作的任务，这些操作可能涉及磁盘操作、网络通信或用户交互等。这类任务的特点是CPU计算不是主要瓶颈，相反，它们大部分时间都在等待外部操作的完成，如数据读写、数据传输等。

### 举例说明

1. **文件处理**：例如，一个脚本读取和写入大量数据到硬盘上的多个文件中。这类任务的速度往往受限于磁盘的读写速度，而不是CPU的处理速度。
2. **数据库操作**：大规模的数据库查询和事务处理，这些操作包括大量的磁盘I/O操作，以及可能的网络I/O（如果数据库被远程访问）。
3. **网络通信**：如Web服务器处理HTTP请求，服务器主要在进行网络数据的发送和接收，特别是当处理大量小文件或数据包时。
4. **用户界面**：涉及频繁的用户交互操作，如GUI应用程序，主要等待用户的输入操作，如鼠标点击和键盘输入。

### I/O密集型任务的处理策略

由于I/O密集型任务的瓶颈主要在于等待I/O操作，而不是CPU计算，因此优化这类任务通常关注于减少I/O操作的延迟和等待时间，策略包括：

1. **使用异步I/O操作**：异步I/O可以让程序在等待I/O操作完成时继续执行其他任务，不阻塞程序的主流程。这样可以显著提高程序的效率和响应性。
2. **多线程或多进程**：通过并行处理多个I/O操作，可以同时执行多个I/O请求，从而提高应用程序的整体效率。例如，一个Web服务器通常会为每个入站的客户端请求启动一个新的线程或进程。
3. **缓存技术**：通过缓存频繁访问的数据到内存中，减少对磁盘的读写次数，可以减少I/O请求的时间。
4. **优化I/O性能**：比如使用更快的硬件（SSD而不是HDD）、增加网络带宽、优化数据库索引等。

理解I/O密集型任务的特点及其对资源的具体需求，有助于更好地设计和调优系统，提高应用性能。





I/O 密集型任务的特点就是程序会经常性的因为 I/O 操作而进入阻塞状态，比如我们之前使用 `requests`获取页面代码或二进制内容，发出一个请求之后，程序必须要等待网站返回响应之后才能继续运行，如果目标网站不是很给力或者网络状况不是很理想，那么等待响应的时间可能会很久，而在这个过程中整个程序是一直阻塞在那里，没有做任何的事情。通过前面的课程，我们已经知道了可以通过多线程的方式为爬虫提速，使用多线程的本质就是，当一个线程阻塞的时候，程序还有其他的线程可以继续运转，因此整个程序就不会在阻塞和等待中浪费了大量的时间。

事实上，还有一种非常适合 I/O 密集型任务的并发编程方式，我们称之为异步编程，你也可以将它称为异步 I/O。这种方式并不需要启动多个线程或多个进程来实现并发，它是通过多个子程序相互协作的方式来提升 CPU 的利用率，解决了 I/O 密集型任务 CPU  利用率很低的问题，我一般将这种方式称为“协作式并发”。这里，我不打算探讨操作系统的各种 I/O 模式，因为这对很多读者来说都太过抽象；但是我们得先抛出两组概念给大家，一组叫做“阻塞”和“非阻塞”，一组叫做“同步”和“异步”。

### 基本概念

#### 阻塞

阻塞状态指程序未得到所需计算资源时被挂起的状态。程序在等待某个操作完成期间，自身无法继续处理其他的事情，则称该程序在该操作上是阻塞的。阻塞随时都可能发生，最典型的就是 I/O 中断（包括网络 I/O 、磁盘 I/O 、用户输入等）、休眠操作、等待某个线程执行结束，甚至包括在 CPU 切换上下文时，程序都无法真正的执行，这就是所谓的阻塞。

#### 非阻塞

程序在等待某操作过程中，自身不被阻塞，可以继续处理其他的事情，则称该程序在该操作上是非阻塞的。非阻塞并不是在任何程序级别、任何情况下都可以存在的。仅当程序封装的级别可以囊括独立的子程序单元时，它才可能存在非阻塞状态。显然，某个操作的阻塞可能会导程序耗时以及效率低下，所以我们会希望把它变成非阻塞的。

#### 同步

不同程序单元为了完成某个任务，在执行过程中需靠某种通信方式以协调一致，我们称这些程序单元是同步执行的。例如前面讲过的给银行账户存钱的操作，我们在代码中使用了“锁”作为通信信号，让多个存钱操作强制排队顺序执行，这就是所谓的同步。

#### 异步

不同程序单元在执行过程中无需通信协调，也能够完成一个任务，这种方式我们就称之为异步。例如，使用爬虫下载页面时，调度程序调用下载程序后，即可调度其他任务，而无需与该下载任务保持通信以协调行为。不同网页的下载、保存等操作都是不相关的，也无需相互通知协调。很显然，异步操作的完成时刻和先后顺序并不能确定。

很多人都不太能准确的把握这几个概念，这里我们简单的总结一下，同步与异步的关注点是**消息通信机制**，最终表现出来的是“有序”和“无序”的区别；阻塞和非阻塞的关注点是**程序在等待消息时状态**，最终表现出来的是程序在等待时能不能做点别的。如果想深入理解这些内容，推荐大家阅读经典著作[《UNIX网络编程》](https://item.jd.com/11880047.html)，这本书非常的赞。



在计算和通信中，**同步（Synchronous）** 和 **异步（Asynchronous）** 是描述交互方式和时间管理的两个基本概念。这些术语通常用于描述操作的执行方式，特别是在涉及输入/输出操作、消息传递和其他延迟敏感的活动中。以下是对这两个概念的详细解释和对比：

### 同步（Synchronous）

在同步操作中，任务或操作的执行必须在一个完成后才能开始另一个。这意味着执行操作的过程中会阻塞或等待每个操作的完成。在同步模式下，操作一步接一步地进行，每个步骤都依赖于前一个步骤的完成。

**特点：**

- **阻塞操作**：在等待操作如I/O（输入/输出）、数据库查询或网络请求完成期间，程序或线程会停止执行后续代码。
- **简单直接的执行流**：编程模型简单，逻辑顺序明确，易于理解和调试，因为代码的执行顺序与书写顺序一致。
- **资源利用率低**：在等待外部操作完成时，CPU可能处于空闲状态，这导致资源利用不充分。

**应用示例：**

- 从硬盘读取文件内容并等待操作完成后才执行下一步。
- 在Web应用中，服务器处理请求，需要查询数据库并等待结果才能继续处理。

### 异步（Asynchronous）

异步操作允许任务在等待另一个任务完成的同时继续执行，不需要阻塞等待。这种方式特别适用于依赖长时间等待的操作，如网络请求、文件I/O等。异步模型提高了程序的整体效率和响应性。

**特点：**

- **非阻塞操作**：调用者启动一个操作后可以直接继续执行下一个命令，而不用等待前一个操作完成。
- **复杂的控制流**：异步编程可能涉及回调、事件、消息队列等技术来处理操作完成后的活动，这可能使得程序逻辑较难跟踪和维护。
- **高效的资源利用**：CPU可以在等待操作完成时继续处理其他任务，从而更有效地利用计算资源。

**应用示例：**

- 在GUI应用中，界面需要保持响应用户输入，同时可能需要进行长时间的数据加载。
- Web服务器并发处理成千上万的客户端请求，而不是一次处理一个。

### 比较

- **效率**：异步通常更有效率，尤其是在涉及多个可能延迟的I/O操作时。
- **复杂度**：同步编程比异步编程简单，因为它不涉及处理程序的多个执行分支。
- **适用场景**：如果操作包含许多等待时间，例如大量的磁盘操作或网络请求，使用异步可以显著提升性能和用户体验。而在一些线性任务和简单的逻辑中使用同步可能会更直观易懂。

理解同步和异步的区别及其适用场景对于开发高效和响应式的应用程序至关重要。




### 生成器和协程

前面我们说过，异步编程是一种“协作式并发”，即通过多个子程序相互协作的方式提升 CPU 的利用率，从而减少程序在阻塞和等待中浪费的时间，最终达到并发的效果。我们可以将多个相互协作的子程序称为“协程”，它是实现异步编程的关键。在介绍协程之前，我们先通过下面的代码，看看什么是生成器。

```Python
def fib(max_count):
    a, b = 0, 1
    for _ in range(max_count):
        a, b = b, a + b
        yield a
```

上面我们编写了一个生成斐波那契数列的生成器，调用上面的 `fib`函数并不是执行该函数获得返回值，因为 `fib`函数中有一个特殊的关键字 `yield`。这个关键字使得 `fib`函数跟普通的函数有些区别，调用该函数会得到一个生成器对象，我们可以通过下面的代码来验证这一点。

```Python
gen_obj = fib(20)
print(gen_obj)
```

输出：

```
<generator object fib at 0x106daee40>
```

我们可以使用内置函数 `next`从生成器对象中获取斐波那契数列的值，也可以通过 `for-in`循环对生成器能够提供的值进行遍历，代码如下所示。

```Python
for value in gen_obj:
    print(value)
```

生成器经过预激活，就是一个协程，它可以跟其他子程序协作。

```Python
def calc_average():
    total, counter = 0, 0
    avg_value = None
    while True:
        curr_value = yield avg_value
        total += curr_value
        counter += 1
        avg_value = total / counter


def main():
    obj = calc_average()
    # 生成器预激活
    obj.send(None)
    for _ in range(5):
        print(obj.send(float(input())))


if __name__ == '__main__':
    main()
```

上面的 `main`函数首先通过生成器对象的 `send`方法发送一个 `None`值来将其激活为协程，也可以通过 `next(obj)`达到同样的效果。接下来，协程对象会接收 `main`函数发送的数据并产出（`yield`）数据的平均值。通过上面的例子，不知道大家是否看出两段子程序是怎么“协作”的。

### 异步函数

Python 3.5版本中，引入了两个非常有意思的元素，一个叫 `async`，一个叫 `await`，它们在Python 3.7版本中成为了正式的关键字。通过这两个关键字，可以简化协程代码的编写，可以用更为简单的方式让多个子程序很好的协作起来。我们通过一个例子来加以说明，请大家先看看下面的代码。

```Python
import time


def display(num):
    time.sleep(1)
    print(num)


def main():
    start = time.time()
    for i in range(1, 10):
        display(i)
    end = time.time()
    print(f'{end - start:.3f}秒')


if __name__ == '__main__':
    main()
```

上面的代码每次执行都会依次输出 `1`到 `9`的数字，每个间隔 `1`秒钟，整个代码需要执行大概需要 `9`秒多的时间，这一点我相信大家都能看懂。不知道大家是否意识到，这段代码就是以同步和阻塞的方式执行的，同步可以从代码的输出看出来，而阻塞是指在调用 `display`函数发生休眠时，整个代码的其他部分都不能继续执行，必须等待休眠结束。

接下来，我们尝试用异步的方式改写上面的代码，让 `display`函数以异步的方式运转。

```Python
import asyncio
import time


async def display(num):
    await asyncio.sleep(1)
    print(num)


def main():
    start = time.time()
    objs = [display(i) for i in range(1, 10)]
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(objs))
    loop.close()
    end = time.time()
    print(f'{end - start:.3f}秒')


if __name__ == '__main__':
    main()
```

Python 中的 `asyncio`模块提供了对异步 I/O 的支持。上面的代码中，我们首先在 `display`函数前面加上了 `async`关键字使其变成一个异步函数，调用异步函数不会执行函数体而是获得一个协程对象。我们将 `display`函数中的 `time.sleep(1)`修改为 `await asyncio.sleep(1)`，二者的区别在于，后者不会让整个代码陷入阻塞，因为 `await`操作会让其他协作的子程序有获得 CPU 资源而得以运转的机会。为了让这些子程序可以协作起来，我们需要将他们放到一个事件循环（实现消息分派传递的系统）上，因为**当协程遭遇 I/O 操作阻塞时，就会到事件循环中监听 I/O 操作是否完成，并注册自身的上下文以及自身的唤醒函数（以便恢复执行），之后该协程就变为阻塞状态**。上面的第12行代码创建了 `9`个协程对象并放到一个列表中，第13行代码通过 `asyncio`模块的 `get_event_loop`函数获得了系统的事件循环，第14行通过 `asyncio`模块的 `run_until_complete`函数将协程对象挂载到事件循环上。执行上面的代码会发现，`9`个分别会阻塞 `1`秒钟的协程总共只阻塞了约 `1`秒种的时间，因为**阻塞的协程对象会放弃对 CPU 的占有而不是让 CPU 处于闲置状态，这种方式大大的提升了 CPU 的利用率**。而且我们还会注意到，数字并不是按照从 `1`到 `9`的顺序打印输出的，这正是我们想要的结果，说明它们是**异步执行**的。对于爬虫这样的 I/O 密集型任务来说，这种协作式并发在很多场景下是比使用多线程更好的选择，因为这种做法减少了管理和维护多个线程以及多个线程切换所带来的开销。

### aiohttp库

我们之前使用的 `requests`三方库并不支持异步 I/O，如果希望使用异步 I/O 的方式来加速爬虫代码的执行，我们可以安装和使用名为 `aiohttp`的三方库。

安装 `aiohttp`。

```Bash
pip install aiohttp
```

下面的代码使用 `aiohttp`抓取了 `10`个网站的首页并解析出它们的标题。

```Python
import asyncio
import re

import aiohttp
from aiohttp import ClientSession

TITLE_PATTERN = re.compile(r'<title.*?>(.*?)</title>', re.DOTALL)


async def fetch_page_title(url):
    async with aiohttp.ClientSession(headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
    }) as session:  # type: ClientSession
        async with session.get(url, ssl=False) as resp:
            if resp.status == 200:
                html_code = await resp.text()
                matcher = TITLE_PATTERN.search(html_code)
                title = matcher.group(1).strip()
                print(title)


def main():
    urls = [
        'https://www.python.org/',
        'https://www.jd.com/',
        'https://www.baidu.com/',
        'https://www.taobao.com/',
        'https://git-scm.com/',
        'https://www.sohu.com/',
        'https://gitee.com/',
        'https://www.amazon.com/',
        'https://www.usa.gov/',
        'https://www.nasa.gov/'
    ]
    objs = [fetch_page_title(url) for url in urls]
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(objs))
    loop.close()


if __name__ == '__main__':
    main()
```

输出：

```
京东(JD.COM)-正品低价、品质保障、配送及时、轻松购物！
搜狐
淘宝网 - 淘！我喜欢
百度一下，你就知道
Gitee - 基于 Git 的代码托管和研发协作平台
Git
NASA
Official Guide to Government Information and Services   | USAGov
Amazon.com. Spend less. Smile more.
Welcome to Python.org
```

从上面的输出可以看出，网站首页标题的输出顺序跟它们的 URL 在列表中的顺序没有关系。代码的第11行到第13行创建了 `ClientSession`对象，通过它的 `get`方法可以向指定的 URL 发起请求，如第14行所示，跟 `requests`中的 `Session`对象并没有本质区别，唯一的区别是这里使用了异步上下文。代码第16行的 `await`会让因为 I/O 操作阻塞的子程序放弃对 CPU 的占用，这使得其他的子程序可以运转起来去抓取页面。代码的第17行和第18行使用了正则表达式捕获组操作解析网页标题。`fetch_page_title`是一个被 `async`关键字修饰的异步函数，调用该函数会获得协程对象，如代码第35行所示。后面的代码跟之前的例子没有什么区别，相信大家能够理解。

大家可以尝试将 `aiohttp`换回到 `requests`，看看不使用异步 I/O 也不使用多线程，到底和上面的代码有什么区别，相信通过这样的对比，大家能够更深刻的理解我们之前强调的几个概念：同步和异步，阻塞和非阻塞。
