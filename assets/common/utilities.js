// This file is part of Happyschool.
//
// Happyschool is the legal property of its developers, whose names
// can be found in the AUTHORS file distributed with this source
// distribution.
//
// Happyschool is free software: you can redistribute it and/or modify
// it under the terms of the GNU Affero General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// Happyschool is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU Affero General Public License for more details.
//
// You should have received a copy of the GNU Affero General Public License
// along with Happyschool.  If not, see <http://www.gnu.org/licenses/>.

function countCurrentTeaching(app) {
    // eslint-disable-next-line no-undef
    let teachings = user_properties.teaching;
    if ("settings" in app.$store.state) {
        teachings = teachings.filter(value => app.$store.state.settings.teachings.includes(value));
    }
    return teachings.length;
}

export function displayStudent(student) {
    if (countCurrentTeaching(this) === 1) {
        const classeStr = student.classe ? `${student.classe.year}${student.classe.letter.toUpperCase()}` : "(Ancien)";
        return `${student.last_name} ${student.first_name} ${classeStr}`;
    } else {
        return student.display;
    }
}

export function displayClasse(classe) {
    if (countCurrentTeaching(this) === 1) {
        return `${classe.year}${classe.letter.toUpperCase()}`;
    } else {
        return `${classe.year}${classe.letter.toUpperCase()} – ${classe.teaching.display_name}`;
    }
}
