""" Helper functions that make constructing hardware easier.

The set of functions includes

* `as_wires`: converts consts to wires if needed (and does nothing to wires)
* `probe`: a way to check the values of wires during simulation time
* `rtl_assert`: Simulation time hardware value assertions

"""

from __future__ import print_function, unicode_literals

import six
import math

from .core import working_block, _NameIndexer
from .pyrtlexceptions import PyrtlError, PyrtlInternalError
from .wire import WireVector, Input, Output, Const, Register
from pyrtl.rtllib import barrel

# -----------------------------------------------------------------
#        ___       __   ___  __   __
#  |__| |__  |    |__) |__  |__) /__`
#  |  | |___ |___ |    |___ |  \ .__/
#


def input_list(names, bitwidth=1):
    """ Allocate and return a list of Inputs. """
    return wirevector_list(names, bitwidth, wvtype=Input)


def output_list(names, bitwidth=1):
    """ Allocate and return a list of Outputs. """
    return wirevector_list(names, bitwidth, wvtype=Output)


def register_list(names, bitwidth=1):
    """ Allocate and return a list of Registers. """
    return wirevector_list(names, bitwidth, wvtype=Register)


def wirevector_list(names, bitwidth=1, wvtype=WireVector):
    """ Allocate and return a list of WireVectors. """
    if '/' in names and bitwidth != 1:
        raise PyrtlError('only one of optional "/" or bitwidth parameter allowed')
    names = names.replace(',', ' ')

    wirelist = []
    for fullname in names.split():
        try:
            name, bw = fullname.split('/')
        except:
            name, bw = fullname, bitwidth
        wirelist.append(wvtype(bitwidth=bw, name=name))
    return wirelist


def mult_signed(a, b):
    """ Return a*b where a and b are treated as signed values. """
    a, b = as_wires(a), as_wires(b)
    final_len = len(a) + len(b)
    # sign extend both inputs to the final target length
    a, b = a.sign_extended(final_len), b.sign_extended(final_len)
    # the result is the multiplication of both, but truncated
    # TODO: this may make estimates based on the multiplication overly
    # pessimistic as half of the multiply result is thrown right away!
    return (a * b)[0:final_len]


def as_wires(val, bitwidth=None, truncating=True, block=None):
    """ Return wires from val which may be wires, integers, strings, or bools.

    :param val: a wirevector-like object or something that can be converted into
      a Const
    :param bitwidth: The bitwidth the resulting wire should be
    :param bool truncating: determines whether bits will be dropped to achieve
     the desired bitwidth if it is too long (if true, the most-significant bits
     will be dropped)
    :param Block block: block to use for wire

    This function is mainly used to coerce values into WireVectors (for
    example, operations such as "x+1" where "1" needs to be converted to
    a Const WireVector).
    """
    from .memory import _MemIndexed
    block = working_block(block)

    if isinstance(val, (int, six.string_types)):
        # note that this case captures bool as well (as bools are instances of ints)
        return Const(val, bitwidth=bitwidth, block=block)
    elif isinstance(val, _MemIndexed):
        # convert to a memory read when the value is actually used
        if val.wire is None:
            val.wire = as_wires(val.mem._readaccess(val.index), bitwidth, truncating, block)
        return val.wire
    elif not isinstance(val, WireVector):
        raise PyrtlError('error, expecting a wirevector, int, or verilog-style '
                         'const string got %s instead' % repr(val))
    elif bitwidth == '0':
        raise PyrtlError('error, bitwidth must be >= 1')
    elif val.bitwidth is None:
        raise PyrtlError('error, attempting to use wirevector with no defined bitwidth')
    elif bitwidth and bitwidth > val.bitwidth:
        return val.zero_extended(bitwidth)
    elif bitwidth and truncating and bitwidth < val.bitwidth:
        return val[:bitwidth]  # truncate the upper bits
    else:
        return val


def match_bitwidth(*args, **opt):
    """ Matches the bitwidth of all of the input arguments with zero or sign extend

    :param args: WireVectors of which to match bitwidths
    :param opt: Optional keyword argument 'signed=True' (defaults to False)
    :return: tuple of args in order with extended bits
    """
    # TODO: when we drop 2.7 support, this code should be cleaned up with explicit
    # kwarg support for "signed" rather than the less than helpful "**opt"
    if len(opt) == 0:
        signed = False
    else:
        if len(opt) > 1 or 'signed' not in opt:
            raise PyrtlError('error, only supported kwarg to match_bitwidth is "signed"')
        signed = bool(opt['signed'])

    max_len = max(len(wv) for wv in args)
    if signed:
        return (wv.sign_extended(max_len) for wv in args)
    else:
        return (wv.zero_extended(max_len) for wv in args)


def signed_lt(a, b):
    """ Return a single bit result of signed less than comparison. """
    a, b = match_bitwidth(as_wires(a), as_wires(b), signed=True)
    r = a - b
    return r[-1] ^ (~a[-1])


def signed_le(a, b):
    """ Return a single bit result of signed less than or equal comparison. """
    a, b = match_bitwidth(as_wires(a), as_wires(b), signed=True)
    r = a - b
    return (r[-1] ^ (~a[-1])) | (a == b)


def signed_gt(a, b):
    """ Return a single bit result of signed greater than comparison. """
    a, b = match_bitwidth(as_wires(a), as_wires(b), signed=True)
    r = b - a
    return r[-1] ^ (~b[-1])


def signed_ge(a, b):
    """ Return a single bit result of signed greater than or equal comparison. """
    a, b = match_bitwidth(as_wires(a), as_wires(b), signed=True)
    r = b - a
    return (r[-1] ^ (~b[-1])) | (a == b)


def _check_shift_inputs(a, shamt):
    # TODO: perhaps this should just be implemented directly rather than throwing error
    if isinstance(shamt, int):
        raise PyrtlError('shift_amount is an integer, use slice instead')
    if isinstance(shamt, Const):
        raise PyrtlError('shift_amount is a constant, use slice instead')
    a, shamt = as_wires(a), as_wires(shamt)
    log_length = int(math.log(len(a)-1, 2))  # note the one offset
    # TODO: perhaps this should just be implemented directly rather than throwing error
    if len(shamt) > log_length:
        raise PyrtlError('the shift_amount wirevector is providing bits '
                         'that would shift the value off the end')
    return a, shamt


def shift_left_arithmetic(bits_to_shift, shift_amount):
    """ Shift left arithmetic operation.

    :param bits_to_shift: WireVector to shift left
    :param shift_amount: WireVector specifying amount to shift
    :return: WireVector of same length as bits_to_shift

    This function returns a new WireVector of length equal to the length
    of the input `bits_to_shift` but where the bits have been shifted
    to the left.  An arithemetic shift is one that treats the value as
    as signed number, although for left shift arithmetic and logic shift
    are identical.  Note that `shift_amount` is treated as unsigned.
    """
    # shift left arithmetic and logical are the same thing
    return shift_left_logical(bits_to_shift, shift_amount)


def shift_right_arithmetic(bits_to_shift, shift_amount):
    """ Shift right arithmetic operation.

    :param bits_to_shift: WireVector to shift right
    :param shift_amount: WireVector specifying amount to shift
    :return: WireVector of same length as bits_to_shift

    This function returns a new WireVector of length equal to the length
    of the input `bits_to_shift` but where the bits have been shifted
    to the right.  An arithemetic shift is one that treats the value as
    as signed number, meaning the sign bit (the most significant bit of
    `bits_to_shift`) is shifted in. Note that `shift_amount` is treated as
    unsigned.
    """
    a, shamt = _check_shift_inputs(bits_to_shift, shift_amount)
    bit_in = bits_to_shift[-1]  # shift in sign_bit
    dir = Const(0)  # shift right
    return barrel.barrel_shifter(bits_to_shift, bit_in, dir, shift_amount)


def shift_left_logical(bits_to_shift, shift_amount):
    """ Shift left logical operation.

    :param bits_to_shift: WireVector to shift left
    :param shift_amount: WireVector specifying amount to shift
    :return: WireVector of same length as bits_to_shift

    This function returns a new WireVector of length equal to the length
    of the input `bits_to_shift` but where the bits have been shifted
    to the left.  An logical shift is one that treats the value as
    as unsigned number, meaning the zeros are shifted in.  Note that
    `shift_amount` is treated as unsigned.
    """
    a, shamt = _check_shift_inputs(bits_to_shift, shift_amount)
    bit_in = Const(0)  # shift in a 0
    dir = Const(1)  # shift left
    return barrel.barrel_shifter(bits_to_shift, bit_in, dir, shift_amount)


def shift_right_logical(bits_to_shift, shift_amount):
    """ Shift right logical operation.

    :param bits_to_shift: WireVector to shift left
    :param shift_amount: WireVector specifying amount to shift
    :return: WireVector of same length as bits_to_shift

    This function returns a new WireVector of length equal to the length
    of the input `bits_to_shift` but where the bits have been shifted
    to the right.  An logical shift is one that treats the value as
    as unsigned number, meaning the zeros are shifted in regardless of
    the "sign bit".  Note that `shift_amount` is treated as unsigned.
    """
    a, shamt = _check_shift_inputs(bits_to_shift, shift_amount)
    bit_in = Const(0)  # shift in a 0
    dir = Const(0)  # shift right
    return barrel.barrel_shifter(bits_to_shift, bit_in, dir, shift_amount)


probeIndexer = _NameIndexer('Probe-')


def probe(w, name=None):
    """ Print useful information about a WireVector when in debug mode.

    :param w: WireVector from which to get info
    :param name: optional name for probe (defaults to an autogenerated name)
    :return: original WireVector w

    Probe can be inserted into a existing design easily as it returns the
    original wire unmodified. For example ``y <<= x[0:3] + 4`` could be turned
    into ``y <<= probe(x)[0:3] + 4`` to give visibility into both the origin of
    ``x`` (including the line that WireVector was originally created) and
    the run-time values of ``x`` (which will be named and thus show up by
    default in a trace.  Likewise ``y <<= probe(x[0:3]) + 4``,
    ``y <<= probe(x[0:3] + 4)``, and ``probe(y) <<= x[0:3] + 4`` are all
    valid uses of `probe`.

    Note: `probe` does actually add a wire to the working block of w (which can
    confuse various post-processing transforms such as output to verilog).
    """
    if not isinstance(w, WireVector):
        raise PyrtlError('Only WireVectors can be probed')

    if name is None:
        name = '(%s: %s)' % (probeIndexer.make_valid_string(), w.name)
    print("Probe: " + name + ' ' + get_stack(w))

    p = Output(name=name)
    p <<= w  # late assigns len from w automatically
    return w


def get_stacks(*wires):
    call_stack = getattr(wires[0], 'init_call_stack', None)
    if not call_stack:
        return '    No call info found for wires: use set_debug_mode() ' \
               'to provide more information\n'
    else:
        return '\n'.join(str(wire) + ":\n" + get_stack(wire) for wire in wires)


def get_stack(wire):
    if not isinstance(wire, WireVector):
        raise PyrtlError('Only WireVectors can be traced')

    call_stack = getattr(wire, 'init_call_stack', None)
    if call_stack:
        frames = ' '.join(frame for frame in call_stack[:-1])
        return "Wire Traceback, most recent call last \n" + frames + "\n"
    else:
        return '    No call info found for wire: use set_debug_mode()'\
               ' to provide more information'


assertIndexer = _NameIndexer('assertion')


def rtl_assert(w, exp, block=None):
    """ Add hardware assertions to be checked on the RTL design.

    :param w: should be a WireVector
    :param Exception exp: Exception to throw when assertion fails
    :param Block block: block to which the assertion should be added (default to working block)
    :return: the Output wire for the assertion (can be ignored in most cases)

    If at any time during execution the wire w is not `true` (i.e. asserted low)
    then simulation will raise exp.
    """
    block = working_block(block)

    if not isinstance(w, WireVector):
        raise PyrtlError('Only WireVectors can be asserted with rtl_assert')
    if len(w) != 1:
        raise PyrtlError('rtl_assert checks only a WireVector of bitwidth 1')
    if not isinstance(exp, Exception):
        raise PyrtlError('the second argument to rtl_assert must be an instance of Exception')
    if isinstance(exp, KeyError):
        raise PyrtlError('the second argument to rtl_assert cannot be a KeyError')
    if w not in block.wirevector_set:
        raise PyrtlError('assertion wire not part of the block to which it is being added')
    if w not in block.wirevector_set:
        raise PyrtlError('assertion not a known wirevector in the target block')

    if w in block.rtl_assert_dict:
        raise PyrtlInternalError('assertion conflicts with existing registered assertion')

    assert_wire = Output(bitwidth=1, name=assertIndexer.make_valid_string(), block=block)
    assert_wire <<= w
    block.rtl_assert_dict[assert_wire] = exp
    return assert_wire


def check_rtl_assertions(sim):
    """ Checks the values in sim to see if any registers assertions fail.

    :param sim: Simulation in which to check the assertions
    :return: None
    """

    for (w, exp) in sim.block.rtl_assert_dict.items():
        try:
            value = sim.inspect(w)
            if not value:
                raise exp
        except KeyError:
            pass


def _check_for_loop(block=None):
    block = working_block(block)
    logic_left = block.logic.copy()
    wires_left = block.wirevector_subset(exclude=(Input, Const, Output, Register))
    prev_logic_left = len(logic_left) + 1
    while prev_logic_left > len(logic_left):
        prev_logic_left = len(logic_left)
        nets_to_remove = set()  # bc it's not safe to mutate a set inside its own iterator
        for net in logic_left:
            if not any(n_wire in wires_left for n_wire in net.args):
                nets_to_remove.add(net)
                wires_left.difference_update(net.dests)
        logic_left -= nets_to_remove

    if 0 == len(logic_left):
        return None
    return wires_left, logic_left


def find_loop(block=None):
    block = working_block(block)
    block.sanity_check()  # make sure that the block is sane first

    result = _check_for_loop(block)
    if not result:
        return
    wires_left, logic_left = result
    import random

    class _FilteringState(object):
        def __init__(self, dst_w):
            self.dst_w = dst_w
            self.arg_num = -1

    def dead_end():
        # clean up after a wire is found to not be part of the loop
        wires_left.discard(cur_item.dst_w)
        current_wires.discard(cur_item.dst_w)
        del checking_stack[-1]

    # now making a map to quickly look up nets
    dest_nets = {dest_w: net_ for net_ in logic_left for dest_w in net_.dests}
    initial_w = random.sample(wires_left, 1)[0]

    current_wires = set()
    checking_stack = [_FilteringState(initial_w)]

    # we don't use a recursive method as Python has a limited stack (default: 999 frames)
    while len(checking_stack):
        cur_item = checking_stack[-1]
        if cur_item.arg_num == -1:
            #  first time testing this item
            if cur_item.dst_w not in wires_left:
                dead_end()
                continue
            current_wires.add(cur_item.dst_w)
            cur_item.net = dest_nets[cur_item.dst_w]
            if cur_item.net.op == 'r':
                dead_end()
                continue
        cur_item.arg_num += 1  # go to the next item
        if cur_item.arg_num == len(cur_item.net.args):
            dead_end()
            continue
        next_wire = cur_item.net.args[cur_item.arg_num]
        if next_wire not in current_wires:
            current_wires.add(next_wire)
            checking_stack.append(_FilteringState(next_wire))
        else:  # We have found the loop!!!!!
            loop_info = []
            for f_state in reversed(checking_stack):
                loop_info.append(f_state)
                if f_state.dst_w is next_wire:
                    break
            else:
                raise PyrtlError("Shouldn't get here! Couldn't figure out the loop")
            return loop_info
    raise PyrtlError("Error in detecting loop")


def find_and_print_loop(block=None):
    loop_data = find_loop(block)
    print_loop(loop_data)
    return loop_data


def print_loop(loop_data):
    if not loop_data:
        print("No Loop Found")
    else:
        print("Loop found:")
        print('\n'.join("{}".format(fs.net) for fs in loop_data))
        # print '\n'.join("{} (dest wire: {})".format(fs.net, fs.dst_w) for fs in loop_info)
        print("")


def _currently_in_ipython():
    """ Return true if running under ipython, otherwise return False. """
    try:
        __IPYTHON__  # pylint: disable=undefined-variable
        return True
    except NameError:
        return False


class _NetCount(object):
    """
    Helper class to track when to stop an iteration that depends on number of nets

    Mainly useful for iterations that are for optimization
    """
    def __init__(self, block=None):
        self.block = working_block(block)
        self.prev_nets = len(self.block.logic) * 1000

    def shrank(self, block=None, percent_diff=0, abs_diff=1):
        """
        Returns whether a block has less nets than before

        :param Block block: block to check (if changed)
        :param Number percent_diff: percentage difference threshold
        :param int abs_diff: absolute difference threshold
        :return: boolean

        This function checks whether the change in the number of
        nets is greater than the percentage and absolute difference
        thresholds.
        """
        if block is None:
            block = self.block
        cur_nets = len(block.logic)
        net_goal = self.prev_nets * (1 - percent_diff) - abs_diff
        less_nets = (cur_nets <= net_goal)
        self.prev_nets = cur_nets
        return less_nets

    shrinking = shrank
