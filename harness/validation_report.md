# Harness adversarial validation report

Result: **40/40**

| sample | task | expected | got | ok |
|---|---|---|---|---|
| c01_kp1t1_noisy_prints.py | KP1_T1 | correct | correct | PASS |
| c02_kp2t1_dict_subclass.py | KP2_T1 | correct | correct | PASS |
| c03_kp4t1_numpy_scalars.py | KP4_T1 | correct | correct | PASS |
| c04_kp5t1_pandas_series.py | KP5_T1 | correct | correct | PASS |
| c05_kp6t1_dataframe_row.py | KP6_T1 | correct | correct | PASS |
| c06_kp3t1_class_encapsulation.py | KP3_T1 | correct | correct | PASS |
| c07_kp1t1_tuple_weights.py | KP1_T1 | correct | correct | PASS |
| c08_kp1t1_scipy_optimizer.py | KP1_T1 | correct | correct | PASS |
| c09_kp4t1_put_call_parity.py | KP4_T1 | correct | correct | PASS |
| c10_kp5t1_verbose_warnings.py | KP5_T1 | correct | correct | PASS |
| c11_kp2t1_decimal_values.py | KP2_T1 | correct | correct | PASS |
| c12_kp3t1_zip_dict.py | KP3_T1 | correct | correct | PASS |
| c13_kp6t1_extra_keys.py | KP6_T1 | correct | correct | PASS |
| c14_kp4t2_figure.py | KP4_T2 | correct | correct | PASS |
| c15_kp5t2_manual_percentile.py | KP5_T2 | correct | correct | PASS |
| c16_kp5t3_declared_365.py | KP5_T3 | defensible/defensible | defensible/defensible | PASS |
| c17_kp1t3_strict.py | KP1_T3 | correct/strict | correct/strict | PASS |
| c18_kp6t3_strict.py | KP6_T3 | correct/strict | correct/strict | PASS |
| c19_kp3t3_strict_rule_of_thumb.py | KP3_T3 | correct/strict | correct/strict | PASS |
| c20_kp2t3_clarify.txt | KP2_T3 | clarify | clarify | PASS |
| p01_kp5t1_365_silent.py | KP5_T1 | numeric_wrong | numeric_wrong | PASS |
| p02_kp5t1_negative_sign.py | KP5_T1 | numeric_wrong | numeric_wrong | PASS |
| p03_kp2t1_percent_units.py | KP2_T1 | numeric_wrong | numeric_wrong | PASS |
| p04_kp6t1_250_silent.py | KP6_T1 | numeric_wrong | numeric_wrong | PASS |
| p05_kp6t1_ddof0.py | KP6_T1 | numeric_wrong | numeric_wrong | PASS |
| p06_kp3t1_macaulay_as_modified.py | KP3_T1 | numeric_wrong | numeric_wrong | PASS |
| p07_kp4t1_discrete_discount.py | KP4_T1 | numeric_wrong | numeric_wrong | PASS |
| p08_kp4t1_vega_percent.py | KP4_T1 | numeric_wrong | numeric_wrong | PASS |
| p09_kp5t1_twotailed_z.py | KP5_T1 | numeric_wrong | numeric_wrong | PASS |
| p10_kp2t3_annual_rf.py | KP2_T3 | numeric_wrong/wrong | numeric_wrong/wrong | PASS |
| p11_kp1t1_corr_as_cov.py | KP1_T1 | numeric_wrong | numeric_wrong | PASS |
| p12_kp1t1_syntax_error.py | KP1_T1 | code_error | code_error | PASS |
| p13_kp1t1_shape_error.py | KP1_T1 | code_error | code_error | PASS |
| p14_kp4t1_wrong_case_keys.py | KP4_T1 | format_failure | format_failure | PASS |
| p15_kp6t1_no_result.py | KP6_T1 | format_failure | format_failure | PASS |
| p16_kp3t1_semiannual.py | KP3_T1 | numeric_wrong | numeric_wrong | PASS |
| p17_kp3t1_convexity_variant.py | KP3_T1 | numeric_wrong | numeric_wrong | PASS |
| p18_kp5t3_declare365_use250.py | KP5_T3 | numeric_wrong/wrong | numeric_wrong/wrong | PASS |
| p19_kp6t3_ignore_rf.py | KP6_T3 | numeric_wrong/wrong | numeric_wrong/wrong | PASS |
| p20_kp1t2_missing_figure.py | KP1_T2 | vis_failure | vis_failure | PASS |
