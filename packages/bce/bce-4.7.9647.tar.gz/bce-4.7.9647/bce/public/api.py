#!/usr/bin/env python
#
#  Copyright 2014 - 2018 The BCE Authors. All rights reserved.
#  Use of this source code is governed by a BSD-style license that can be
#  found in the license.txt file.
#

import bce.logic.balancer.main as _lgc_bce_main
import bce.logic.common.error as _lgc_cm_error
import bce.parser.common.error as _ps_cm_error
import bce.parser.interface.cexp_parser as _ps_cexp_interface
import bce.parser.interface.option as _interface_opt
import bce.parser.interface.printer as _interface_printer
import bce.public.exception as _pub_exception
import bce.public.printer as _pub_printer
import bce.utils.input_checker as _util_input_chk
import types as _types


def _print_cexp(
        cexp_object,
        cexp_parser,
        molecule_parser,
        mexp_parser,
        printer=_pub_printer.PRINTER_TEXT,
        unknown_header="X"
):
    """Print a chemical equation object.

    :type cexp_object: bce.parser.interface.cexp_parser.ChemicalEquation
    :type cexp_parser: bce.parser.interface.cexp_parser.ChemicalEquationParserInterface
    :type molecule_parser: bce.parser.interface.molecule_parser.MoleculeParserInterface
    :type mexp_parser: bce.parser.interface.mexp_parser.MathExpressionParserInterface
    :type printer: int
    :type unknown_header: str
    :param cexp_object: The chemical equation object.
    :param cexp_parser: The CEXP parser.
    :param molecule_parser: The molecule parser.
    :param mexp_parser: The MEXP parser.
    :param printer: The printer ID.
    :param unknown_header: The header of unknowns.
    :rtype : str | dict[str, str]
    :return: The printed string (or bundle).
    """

    #  Create output bundle.
    everything = {}

    #  Print text.
    if (printer & _pub_printer.PRINTER_TEXT) != 0:
        output = cexp_parser.print_out(
            cexp_object,
            molecule_parser,
            mexp_parser,
            printer_type=_interface_printer.PRINTER_TYPE_TEXT
        )
        if printer == _pub_printer.PRINTER_TEXT:
            return output
        else:
            everything[_pub_printer.PRINTER_KEY_TEXT] = output

    #  Print MathML.
    if (printer & _pub_printer.PRINTER_MATHML) != 0:
        output = cexp_parser.print_out(
            cexp_object,
            molecule_parser,
            mexp_parser,
            mexp_protected_header_enabled=True,
            mexp_protected_header_prefix=unknown_header,
            printer_type=_interface_printer.PRINTER_TYPE_MATHML
        ).to_string(indent=0)
        if printer == _pub_printer.PRINTER_MATHML:
            return output
        else:
            everything[_pub_printer.PRINTER_KEY_MATHML] = output

    return everything


def balance_chemical_equation(
        expression,
        options,
        printer=_pub_printer.PRINTER_TEXT,
        unknown_header="X",
        callback_before_balance=None,
        callback_after_balance=None,
        callback_context=None
):
    """Balance a chemical equation.

    :type expression: str
    :type options: bce.option.Option
    :type printer: int
    :type unknown_header: str
    :type callback_before_balance: types.FunctionType | None
    :type callback_after_balance: types.FunctionType | None
    :param expression: The chemical equation.
    :param options: The options.
    :param printer: The printer ID.
    :param unknown_header: The header of unknowns.
    :param callback_before_balance: Callback that will be called before balancing.
    :param callback_after_balance: Callback that will be called after balancing.
    :param callback_context: The callback context.
    :rtype: str | dict[str, str]
    :return: The balanced chemical equation.
    """

    #  Check characters.
    if not _util_input_chk.check_input_expression_characters(expression):
        raise _pub_exception.InvalidCharacterException("Invalid character.")

    #  Wrap the parser interface options.
    if_opt = _interface_opt.OptionWrapper(options)

    #  Get the CEXP parser.
    cexp_parser = if_opt.get_cexp_parser()

    try:
        #  Parse the chemical equation.
        cexp_object = cexp_parser.parse(
            expression,
            options,
            mexp_protected_header_enabled=True,
            mexp_protected_header_prefix=unknown_header
        )

        #  Run before balance callback.
        if callback_before_balance is not None and isinstance(callback_before_balance, _types.FunctionType):
            callback_before_balance(callback_context, cexp_object)

        #  Balance the chemical equation.
        _lgc_bce_main.balance_chemical_equation(
            cexp_object,
            options,
            unknown_header=unknown_header
        )

        #  Run after balance callback.
        if callback_after_balance is not None and isinstance(callback_after_balance, _types.FunctionType):
            callback_after_balance(callback_context, cexp_object)

        #  Print.
        return _print_cexp(
            cexp_object,
            if_opt.get_cexp_parser(),
            if_opt.get_molecule_parser(),
            if_opt.get_mexp_parser(),
            printer=printer,
            unknown_header=unknown_header
        )
    except _ps_cm_error.Error as err:
        raise _pub_exception.ParserErrorWrapper(err.to_string())
    except _lgc_cm_error.Error as err:
        raise _pub_exception.LogicErrorWrapper(err.to_string())


def is_chemical_equation_balanced(expression, options):
    """Check whether a chemical equation is balanced.

    :type expression: str
    :type options: bce.option.Option
    :param expression: The chemical equation.
    :param options: The options.
    :rtype : bool
    :return: True if balanced.
    """

    #  Check characters.
    if not _util_input_chk.check_input_expression_characters(expression):
        raise _pub_exception.InvalidCharacterException("Invalid character.")

    #  Wrap the parser interface options.
    if_opt = _interface_opt.OptionWrapper(options)

    #  Get the CEXP parser.
    cexp_parser = if_opt.get_cexp_parser()

    try:
        #  Parse the chemical equation.
        cexp_object = cexp_parser.parse(
            expression,
            options,
            mexp_protected_header_enabled=False
        )

        #  Check whether the chemical equation is balanced.
        return _lgc_bce_main.check_chemical_equation(cexp_object)
    except _ps_cm_error.Error as err:
        raise _pub_exception.ParserErrorWrapper(err.to_string())
    except _lgc_cm_error.Error as err:
        raise _pub_exception.LogicErrorWrapper(err.to_string())


def substitute_chemical_equation(
        expression,
        substitute_map,
        options,
        printer=_pub_printer.PRINTER_TEXT,
        unknown_header="X"
):
    """Substitute a chemical equation.

    :type expression: str
    :type substitute_map: dict
    :type options: bce.option.Option
    :type printer: int
    :type unknown_header: str
    :param expression: The chemical equation.
    :param substitute_map: The substitution map.
    :param options: The options.
    :param printer: The printer ID.
    :param unknown_header: The header of unknowns.
    :rtype : str | dict[str, str]
    :return: The substituted chemical equation.
    """

    #  Check characters.
    if not _util_input_chk.check_input_expression_characters(expression):
        raise _pub_exception.InvalidCharacterException("Invalid character.")

    #  Wrap the parser interface options.
    if_opt = _interface_opt.OptionWrapper(options)

    #  Get the CEXP parser.
    cexp_parser = if_opt.get_cexp_parser()

    try:
        cexp_object = cexp_parser.parse(
            expression,
            options,
            mexp_protected_header_enabled=False
        )
        cexp_object = cexp_parser.substitute(
            cexp_object,
            options,
            substitute_map=substitute_map
        )

        #  Print.
        return _print_cexp(
            cexp_object,
            if_opt.get_cexp_parser(),
            if_opt.get_molecule_parser(),
            if_opt.get_mexp_parser(),
            printer=printer,
            unknown_header=unknown_header
        )
    except _ps_cm_error.Error as err:
        raise _pub_exception.ParserErrorWrapper(err.to_string())
    except _ps_cexp_interface.SubstituteError as err:
        raise _pub_exception.SubstitutionErrorWrapper(str(err))
