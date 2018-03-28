// This file is part of Appyschool.
//
// Appyschool is the legal property of its developers, whose names
// can be found in the AUTHORS file distributed with this source
// distribution.
//
// Appyschool is free software: you can redistribute it and/or modify
// it under the terms of the GNU Affero General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// Appyschool is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU Affero General Public License for more details.
//
// You should have received a copy of the GNU Affero General Public License
// along with Appyschool.  If not, see <http://www.gnu.org/licenses/>.

const ReconnectingWebSocket = require('reconnecting-websocket');
/*
actionResponse is as follow :
{
    stream_name1: {
        action_name1: function_response1(payload),
        action_name2: function_response2(payload),
        …
    },
    stream_name2: {
        action_name1: function_response1(payload),
        action_name2: function_response2(payload),
        …
    },
    …
}

*/
let AppeSocket = class {
    constructor(actionResponse, onOpen) {
        this.rws = new ReconnectingWebSocket("ws://" + window.location.host + "/");

        this.rws.onmessage = function (event) {
            let data = JSON.parse(event.data);
            let stream = data.stream;
            let payload = data.payload;
            let action = payload.action;

            if (stream in actionResponse) {
                if (action in actionResponse[stream]) {
                    actionResponse[stream][action](payload);
                }
            }
        }

        this.rws.onopen = onOpen;
    }

    getList(stream_name, filters, order_by, per_page, page) {
        let msg = {
            stream: stream_name,
            payload: {
                action: "list",
                request_id: "list-" + stream_name,
                data : {
                    'filters': filters,
                    'order_by': order_by,
                    'page': page,
                    'per_page': per_page,
                }
            }
        };
        this.rws.send(JSON.stringify(msg));
    }

    subscribe(stream_name, action_name) {
        let msg = {
            stream: stream_name,
            payload: {
              action: "subscribe",
              data: {
                  action: action_name
              },
              request_id: action_name + "-" + stream_name +"-subscribe"
            }
        }
        this.rws.send(JSON.stringify(msg));
    }

    create(stream_name, new_data) {
        let msg = {
            stream: stream_name,
            payload: {
                action: "create",
                data: new_data,
                request_id: stream_name +"-create"
            }
        }
        this.rws.send(JSON.stringify(msg));
    }

    update(stream_name, id, new_data) {
        let msg = {
            stream: stream_name,
            payload: {
                action: "update",
                data: new_data,
                pk: id,
                request_id: id + stream_name +"-update"
            }
        }
        this.rws.send(JSON.stringify(msg));
    }

    delete(stream_name, id) {
        let msg = {
            stream: stream_name,
            payload: {
              action: "delete",
              pk: id,
              request_id: id + stream_name +"-delete"
            }
        }
        this.rws.send(JSON.stringify(msg));
    }

    send(stream_name, payload_content) {
        let msg = {
            stream: stream_name,
            payload: payload_content
        }
        this.rws.send(JSON.stringify(msg));
    }
}

export {AppeSocket};
