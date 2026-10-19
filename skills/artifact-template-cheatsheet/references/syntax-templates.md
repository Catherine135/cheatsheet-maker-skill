# Syntax and Exercises

## Category-Based and Syntax-Based Structure

When a topic contains parallel categories, complete each category's explanation and syntax before proceeding. Select numbering from the actual hierarchy. For example:

```text
6. Set operations
(1) UNION: in A or B; eliminates duplicates.
SELECT x FROM A UNION SELECT y FROM B;
(2) INTERSECT: in A and B.
SELECT x FROM A INTERSECT SELECT y FROM B;
(3) EXCEPT: in A but not B.
SELECT x FROM A EXCEPT SELECT y FROM B;
```

Apply the same organization to join categories or table modification operations. Do not collect all code blocks first and separate their explanations afterward. These examples illustrate organization; they are not required content for every course.

Within an existing `(1) Concept` that requires several explanations, use `① Syntax:` for the complete block and subsequent markers for its notes. The label is ordinary prose, not code highlighting. Do not number each code line. Direct expansion beneath a Roman-numbered topic may instead use ordinary 1./2./3. points.

A short definition and simple template, such as renaming, can appear directly together without an added Syntax item. A single topic can expand as follows:

```text
VII. Assertion
1. Definition / purpose.
2. Syntax: ...
3. Checking time / cost.
```

These numbers identify ordinary points. Do not insert a blue `1. Assertion` heading that duplicates its parent.

## Template Selection

Use one consolidated template for related syntax actually covered by the course, followed by keyword-by-keyword explanations. Give individual data types separate lines when useful. Preserve the minimum context needed for reuse rather than reproducing a complete application's schema or several queries that differ only in names.

Lecture materials and instructor transcripts define scope. Technical validity does not establish that a construct was taught. If the instructor uses SOME, do not add ANY, synonyms, deductions, or alternative patterns. Resolve suspected template errors against the sources; validation does not authorize additional course content.

For complex queries, distinguish logical interpretation from written clause order when the source or user requires it:

```text
Logical order: FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY
Written order: SELECT → FROM → WHERE → GROUP BY → HAVING → ORDER BY
```

Check conditions, grouping fields, and ordering expressions for validity. Do not generalize one course's SQL sequence to unrelated languages.

## Token-Level Highlighting

- Fixed keywords, specific functions, operators, parentheses, commas, and periods: bold white text on black.
- Replaceable names, aliases, parameters, values, and function placeholders: regular black English text on gray.
- Distinguishing tokens such as MAX, >= ALL, or NOT EXISTS: change only their text color to `95DCF7`, retaining background and weight.
- Explanations, Syntax labels, and markers retain their prose styling.

In `{{T}}.{{attribute}} AS {{output_name}}`, names are gray while the period, spaces, and AS are black. In `VARCHAR({{15}})`, 15 is gray while VARCHAR and parentheses are black. Do not classify tokens solely by capitalization.

## Authorized Exercises

Group exercises by source or shared schema. List every relevant table and column with `Table(column1,column2,...)`, then preserve question order, question meaning, and requested output columns. Complete each instructor-provided method as `Method n — mechanism`, a concise Idea, and full code. Preserve actual multiple solutions and their distinguishing mechanisms; do not invent alternatives.

For output questions, retain the given query and a compact answer. Mark instructor-identified incorrect solutions as WRONG with the relevant distinction. Briefly identify documented oral corrections. Avoid repeating shared data rows or lengthy derivations. Exercises follow the theory without a forced column or page break unless requested.

Report independent tutorial additions before inserting them into nearby theory. Integrated questions remain in the exercise section. Preserve requested duplicate lookup entries rather than omitting an explicit destination because the construct appears elsewhere.
