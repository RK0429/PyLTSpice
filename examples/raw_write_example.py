def test_readme_snippet():
    # -- Start of RawWrite Example --
    import numpy as np

    from kuPyLTSpice import RawRead, RawWrite, Trace

    LW = RawWrite(fastacces=False)
    tx = Trace("time", np.arange(0.0, 3e-3, 997e-11))
    vy = Trace("N001", np.sin(2 * np.pi * tx.data * 10000))
    vz = Trace("N002", np.cos(2 * np.pi * tx.data * 9970))
    LW.add_trace(tx)
    LW.add_trace(vy)
    LW.add_trace(vz)
    LW.save("./testfiles/teste_snippet1.raw")
    # -- End of RawWrite Example --


def test_trc2raw():  # Convert Teledyne-Lecroy trace files to raw files
    # -- Start of Lecroy Raw File into LTspice raw file Example --
    import numpy as np

    from kuPyLTSpice import RawRead, RawWrite, Trace

    f = open(r"./testfiles/Current_Lock_Front_Right_8V.trc")
    raw_type = (
        ""  # Initialization of parameters that need to be overridden by the file header
    )
    wave_size = 0
    for line in f:
        tokens = line.rstrip("\r\n").split(",")
        if len(tokens) == 4:
            if tokens[0] == "Segments" and tokens[2] == "SegmentSize":
                wave_size = int(tokens[1]) * int(tokens[3])
        if len(tokens) == 2:
            if tokens[0] == "Time" and tokens[1] == "Ampl":
                raw_type = "transient"
                break
    if raw_type == "transient" and wave_size > 0:
        data = np.genfromtxt(f, dtype="float,float", delimiter=",", max_rows=wave_size)
        LW = RawWrite()
        LW.add_trace(Trace("time", [x[0] for x in data]))
        LW.add_trace(Trace("Ampl", [x[1] for x in data]))
        LW.save("teste_trc.raw")
    f.close()
    # -- End of Lecroy Raw File into LTspice raw file Example --


def test_axis_sync():  # Test axis sync
    # -- Start of Combining two different time axis --
    import numpy as np

    from kuPyLTSpice import RawRead, RawWrite, Trace

    LW = RawWrite()
    tx = Trace("time", np.arange(0.0, 3e-3, 997e-11))
    vy = Trace("N001", np.sin(2 * np.pi * tx.data * 10000))
    vz = Trace("N002", np.cos(2 * np.pi * tx.data * 9970))
    LW.add_trace(tx)
    LW.add_trace(vy)
    LW.add_trace(vz)
    LW.save("./testfiles/teste_w.raw")
    LR = RawRead("./testfiles/testfile.raw")
    LW.add_traces_from_raw(LR, ("V(out)",), force_axis_alignment=True)
    LW.save("./testfiles/merge.raw")
    test = """
    equal = True
    for ii in range(len(tx)):
        if t[ii] != tx[ii]:
            print(t[ii], tx[ii])
            equal = False
    print(equal)

    v = LR.get_trace('N001')
    max_error = 1.5e-12
    for ii in range(len(vy)):
        err = abs(v[ii] - vy[ii])
        if err > max_error:
            max_error = err
            print(v[ii], vy[ii], v[ii] - vy[ii])
    print(max_error)
    """
    # -- End of Combining two different Raw Files --


def test_write_ac():
    # -- Start of Writing .AC raw files Example --
    from kuPyLTSpice import RawRead, RawWrite, Trace

    LW = RawWrite()
    LR = RawRead("./testfiles/PI_Filter.raw")
    LR1 = RawRead("./testfiles/PI_Filter_resampled.raw")
    LW.add_traces_from_raw(LR, ("V(N002)",))
    LW.add_traces_from_raw(
        LR1, "V(N002)", rename_format="N002_resampled", force_axis_alignment=True
    )
    LW.flag_fastaccess = False
    LW.save("./testfiles/PI_filter_rewritten.raw")
    LW.flag_fastaccess = True
    LW.save("./testfiles/PI_filter_rewritten_fast.raw")
    # -- End of Writing .AC raw files Example --


def test_write_tran():
    # -- Start of creating a subset of a raw file --
    from kuPyLTSpice import RawRead, RawWrite, Trace

    LR = RawRead("./testfiles/TRAN - STEP.raw")
    LW = RawWrite()
    LW.add_traces_from_raw(LR, ("V(out)", "I(C1)"))
    LW.flag_fastaccess = False
    LW.save("./testfiles/TRAN - STEP0_normal.raw")
    LW.flag_fastaccess = True
    LW.save("./testfiles/TRAN - STEP0_fast.raw")
    # -- End of creating a subset of a raw file --


def test_combine_tran():
    # -- Start of Combining two different Raw Files --
    from kuPyLTSpice import RawRead, RawWrite

    LW = RawWrite()
    for tag, raw in (
        ("AD820_15", "./testfiles/Batch_Test_AD820_15.raw"),
        # ("AD820_10", "./testfiles/Batch_Test_AD820_10.raw"),
        ("AD712_15", "./testfiles/Batch_Test_AD712_15.raw"),
        # ("AD712_10", "./testfiles/Batch_Test_AD712_10.raw"),
        # ("AD820_5", "./testfiles/Batch_Test_AD820_5.raw"),
        # ("AD712_5", "./testfiles/Batch_Test_AD712_5.raw"),
    ):
        LR = RawRead(raw)
        LW.add_traces_from_raw(
            LR,
            ("V(out)", "I(R1)"),
            rename_format="{}_{tag}",
            tag=tag,
            force_axis_alignment=True,
        )
    LW.flag_fastaccess = False
    LW.save("./testfiles/Batch_Test_Combine.raw")
    # -- End of Combining two different Raw Files --


test_readme_snippet()
test_axis_sync()
test_write_ac()
test_write_tran()
test_combine_tran()
