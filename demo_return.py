from process_message_system import *
import sys

class Return(MessageProc):

    def main(self):
        super().main()
        print("in main of Return")
        value = self.receive(
            Message(
                'two',
                action=lambda: time.sleep(10)),
            Message(
                'hi',
                action=lambda: 2 * 2))
       	print(value)


if __name__=='__main__': # really do need this
    print("STARTING",os.getpid())
    me = MessageProc()
    me.main()
    example = Return().start()
    print("Example",example)
    me.give(example, 'hi')